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
from datetime import datetime
from threading import RLock

from msfx.lib_back2.task.task import TaskState

class TaskProgress:
    """
    Container for the information about the progress of a task.
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

    def track_paused(self):
        """
        Track the pause of the task execution.
        """
        with self.lock:
            self.progress.state = TaskState.PAUSED

    def track_resumed(self):
        """
        Track resume task execution.
        """
        with self.lock:
            self.progress.state = TaskState.RUNNING

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
