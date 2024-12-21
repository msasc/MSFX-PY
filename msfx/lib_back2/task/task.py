#  Copyright (c) 2024 Miquel Sas.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import time
from abc import ABC, abstractmethod
from enum import Enum

from msfx.lib_back2.task.monitor import TaskMonitor
from msfx.lib_back2.task.concurrent import Atomic

class TaskState(Enum):
    """
    Enumeration of possible task states.
    """
    READY = "READY"
    """ Task is ready to start execution. """
    RUNNING = "RUNNING"
    """ Task is running. """
    PAUSED = "PAUSED"
    """ Task is paused. """
    SUCCEEDED = "SUCCEEDED"
    """ Task has finishes successfully. """
    CANCELLED = "CANCELLED"
    """ Task was cancelled. """
    FAILED = "FAILED"
    """ Task failed with an exception. """

class Task(ABC):
    """
    Root of tasks aimed to be executed in a separate thread.
    """
    def __init__(self, monitor: TaskMonitor = None):
        """
        :param monitor: optional TaskMonitor to track progress.
        """
        self.__monitor = monitor
        self.__cancel_requested = Atomic[bool](False)
        self.__pause_requested = Atomic[bool](False)
        self.__state = Atomic[TaskState](TaskState.READY)
        self.__exception = Atomic[Exception](None)

    def is_monitor(self) -> bool:
        return self.__monitor is not None

    def get_monitor(self) -> TaskMonitor:
        return self.__monitor

    def request_cancel(self):
        self.__cancel_requested.set(True)

    def request_pause(self):
        self.__pause_requested.set(True)

    def request_resume(self):
        self.__pause_requested.set(False)

    def is_cancel_requested(self) -> bool:
        return self.__cancel_requested.get()

    def is_pause_requested(self) -> bool:
        return self.__pause_requested.get()

    def set_cancelled(self):
        self.set_state(TaskState.CANCELLED)

    def is_running(self) -> bool:
        return self.__state.get() == TaskState.RUNNING

    def is_paused(self) -> bool:
        return self.__state.get() == TaskState.PAUSED

    def has_cancelled(self) -> bool:
        return self.__state.get() == TaskState.CANCELLED

    def has_succeeded(self) -> bool:
        return self.__state.get() == TaskState.SUCCEEDED

    def has_failed(self) -> bool:
        return self.__state.get() == TaskState.FAILED

    def has_finished(self) -> bool:
        if self.__state.get() == TaskState.SUCCEEDED:
            return True
        if self.__state.get() == TaskState.CANCELLED:
            return True
        if self.__state.get() == TaskState.FAILED:
            return True
        return False

    def get_state(self) -> TaskState:
        return self.__state.get()

    def set_state(self, state: TaskState):
        self.__state.set(state)

    def get_exception(self) -> Exception or None:
        return self.__exception.get()

    def check_paused(self):
        while True:
            if self.is_pause_requested():
                self.set_state(TaskState.PAUSED)
                self.track_paused()
                time.sleep(0.1)
            else:
                self.set_state(TaskState.RUNNING)
                self.track_resumed()
                break

    def track_started(self):
        if self.__monitor:
            self.__monitor.track_started()

    def track_progress(self, message: str = "", work_done: int = 0, total_work: int = -1):
        if self.__monitor:
            self.__monitor.track_progress(message, work_done, total_work)

    def track_cancelled(self):
        if self.__monitor:
            self.__monitor.track_cancelled()

    def track_paused(self):
        if self.__monitor:
            self.__monitor.track_paused()

    def track_resumed(self):
        if self.__monitor:
            self.__monitor.track_resumed()

    def track_failed(self):
        if self.__monitor:
            self.__monitor.track_failed(self.__exception.get())

    def track_end(self):
        if self.__monitor:
            self.__monitor.track_end(self.__state.get())

    @abstractmethod
    def execute(self):
        pass

    def executeTask(self):
        try:
            # Start running.
            self.set_state(TaskState.RUNNING)
            self.track_started()

            # Launch the effective execution and register any eventual exception.
            self.execute()

        except Exception as e:
            self.__exception.set(e)

        # Register the proper state.
        if self.get_exception() is not None:
            self.set_state(TaskState.FAILED)
        elif self.get_state() != TaskState.CANCELLED:
            self.set_state(TaskState.SUCCEEDED)

        # Track end if a monitor is present.
        self.track_end()

        # Ensure cancel requested does not remain set, the state is enough
        # to know whether the task was cancelled.
        self.__cancel_requested.set(False)
