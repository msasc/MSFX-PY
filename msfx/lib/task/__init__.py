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

from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
from threading import RLock
from typing import Generic, TypeVar

T = TypeVar('T')

class Atomic(Generic[T]):
    """
    Generic atomic reference wit get, set and get_and_set methods.
    """
    def __init__(self, value: T):
        self.__lock = RLock()
        self.__value = value

    def get(self) -> T:
        with self.__lock:
            return self.__value

    def set(self, value: T):
        with self.__lock:
            self.__value = value

    def get_and_set(self, value: T):
        with self.__lock:
            prev_value = self.__value
            self.__value = value
            return prev_value


class TaskState(Enum):
    """
    Enumeration of possible task states.
    """
    READY = "READY"
    """ Task is ready to start execution. """
    RUNNING = "RUNNING"
    """ Task is running. """
    SUCCEEDED = "SUCCEEDED"
    """ Task has finishes successfully. """
    CANCELLED = "CANCELLED"
    """ Task was cancelled. """
    FAILED = "FAILED"
    """ Task failed with an exception. """


class TaskProgress:
    """
    Container for the information about the progress oif a task.
    """
    def __init__(self):
        self.state = None

        self.start_time: datetime or None = None
        self.end_time: datetime or None = None

        self.message: str or None = None
        self.work_done: int or None = None
        self.total_work: int or None = None

        self.exception: Exception or None = None

        self.current_time: datetime or None = None
        self.elapsed_duration: datetime or None = None
        self.expected_duration: datetime or None = None
        self.expected_end_time: datetime or None = None

    def has_finished(self) -> bool:
        if self.state == TaskState.CANCELLED:
            return True
        if self.state == TaskState.FAILED:
            return True
        if self.state == TaskState.SUCCEEDED:
            return True
        return False


class TaskMonitor:
    """
    A TaskMonitor is used to track the progress of a task and retrieve it
    to monitor it on a user interface.
    """
    def __init__(self):
        self.lock: RLock = RLock()
        self.progress: TaskProgress = TaskProgress()

    def track_started(self):
        """
        Just indicate that the task has started.
        """
        with self.lock:
            self.progress.state = TaskState.RUNNING
            self.progress.start_time = datetime.now()

    def track_progress(self, message: str = "", work_done: int = 0, total_work: int = -1):
        """
        Track the progress of the task.
        :param message: Optional message.
        :param work_done: Optional work done or step performed.
        :param total_work: Optional total work to perform or number of steps,
        -1 indicates indeterminate.
        """
        with self.lock:
            self.progress.message = message
            self.progress.work_done = work_done
            self.progress.total_work = total_work

    def track_cancelled(self):
        """
        Track the cancellation of the task execution.
        """
        with self.lock:
            self.progress.state = TaskState.CANCELLED
            self.progress.end_time = datetime.now()
            self.progress.exception = Exception("Cancelled")

    def track_failed(self, exception: Exception):
        """
        Track the failure of the task execution.
        """
        with self.lock:
            self.progress.state = TaskState.FAILED
            self.progress.end_time = datetime.now()
            self.progress.exception = exception

    def track_end(self, state: TaskState):
        """
        Track the successful end of the task execution.
        """
        with self.lock:
            self.progress.state = state
            self.progress.end_time = datetime.now()

    def get_progress(self):
        """
        Return the current progress of the task execution.
        :return: The current progress of the task.
        """
        progress = TaskProgress()

        # Get current status ensuring lock.
        with self.lock:
            progress.state = self.progress.state
            progress.start_time = self.progress.start_time
            progress.end_time = self.progress.end_time
            progress.exception = self.progress.exception
            progress.message = self.progress.message
            progress.work_done = self.progress.work_done
            progress.total_work = self.progress.total_work

        # Complete progress information out of the lock.
        progress.current_time = datetime.now()
        progress.elapsed_duration = progress.current_time - progress.start_time
        if progress.total_work > 0 and progress.work_done > 0:
            work = min(progress.work_done, progress.total_work)
            total = progress.total_work
            elapsed = progress.elapsed_duration
            progress.expected_duration = elapsed * total / work
            progress.expected_end_time = progress.start_time + progress.expected_duration
            if progress.end_time:
                progress.expected_end_time = progress.end_time

        return progress

class Task(ABC):
    def __init__(self, monitor: TaskMonitor = None):
        self.__monitor = monitor
        self.__cancel_requested = Atomic[bool](False)
        self.__state = Atomic[TaskState](TaskState.READY)
        self.__exception = Atomic[Exception](None)

    def is_monitor(self) -> bool:
        return self.__monitor is not None

    def get_monitor(self) -> TaskMonitor:
        return self.__monitor

    def request_cancel(self):
        self.__cancel_requested.set(True)

    def is_cancel_requested(self):
        return self.__cancel_requested.get()

    def set_cancelled(self):
        self.set_state(TaskState.CANCELLED)

    def was_canceled(self) -> bool:
        return self.__state.get() == TaskState.CANCELLED

    def has_succeeded(self) -> bool:
        return self.__state.get() == TaskState.SUCCEEDED

    def get_state(self) -> TaskState:
        return self.__state.get()

    def set_state(self, state: TaskState):
        self.__state.set(state)

    def get_exception(self) -> Exception or None:
        return self.__exception.get()

    def track_started(self):
        if self.__monitor is not None:
            self.__monitor.track_started()

    def track_progress(self, message: str = "", work_done: int = 0, total_work: int = -1):
        if self.__monitor is not None:
            self.__monitor.track_progress(message, work_done, total_work)

    def track_cancelled(self):
        if self.__monitor is not None:
            self.__monitor.track_cancelled()

    def track_failed(self, exception: Exception):
        if self.__monitor is not None:
            self.__monitor.track_failed(self.__exception.get())

    def track_end(self):
        if self.__monitor is not None:
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
