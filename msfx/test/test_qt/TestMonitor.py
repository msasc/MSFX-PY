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

"""
This code is the basis for building the components to execute tasks on threads
and monitoring the execution.

The UI has a main button that starts the task, and a status bar where a label
and a progress bar are installed.

The task is run in a separate thread, and the progress data is stored in the
monitor data object. At the same time, when the task starts, a QTimer is started
to periodically read the monitor data and display the progress.
"""
import sys
from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
from threading import RLock
from typing import Generic, TypeVar

from msfx.lib import qt

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QStatusBar, QLabel, QProgressBar, QWidget, QPushButton, QVBoxLayout, QSizePolicy
)
from PyQt6.QtGui import (
    QGuiApplication, QFont
)
from PyQt6.QtCore import (
    Qt
)
T = TypeVar('T')

# Define a generic class
class Atomic(Generic[T]):
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
    """ Enumeration of possible task states. """
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

    def track_end(self):
        """
        Track the successful end of the task execution.
        """
        with self.lock:
            self.progress.state = TaskState.SUCCEEDED
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

    def get_monitor(self) -> TaskMonitor:
        return self.__monitor

    def request_cancel(self):
        self.__cancel_requested.set(True)

    def is_cancel_requested(self):
        return self.__cancel_requested.get()

    @abstractmethod
    def execute(self):
        pass

    def launch_execute(self):
        x = 0


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My first window")

        # Central widget
        self.buttonTask = QPushButton("Start task")
        self.buttonTask.setFixedSize(200, 100)
        # self.buttonTask.setFont(QFont("Century", 20))
        self.buttonTask.setStyleSheet("QPushButton { font-family: Century; font-size: 20pt; }")

        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.buttonTask, alignment=Qt.AlignmentFlag.AlignCenter)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.setStyleSheet("QStatusBar{border-top: 1px solid rgb(160,180,180);}")

if __name__ == "__main__":
    app = QApplication([])
    screen = QGuiApplication.primaryScreen()
    window = Window()
    qt.setWidgetSize(window, 0.6, 0.6)
    window.show()
    sys.exit(app.exec())
