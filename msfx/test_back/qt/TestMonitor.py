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
import time
from threading import Thread

from PyQt6.QtCore import (
    Qt, QTimer, QEvent
)
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStatusBar,
    QLabel,
    QProgressBar,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout
)

import msfx.lib_back2.qt
from msfx.lib_back2.task.monitor import TaskProgress, TaskMonitor
from msfx.lib_back2.task.task import Task

# Define a generic class
class TaskTestMonitor(Task):
    def __init__(self, monitor: TaskMonitor):
        super().__init__(monitor)

    def execute(self):
        sleep = 0.001
        total_work = 10000
        for work_done in range(total_work):

            if self.is_cancel_requested():
                self.set_cancelled()
                break

            self.check_paused()

            if work_done % 10 == 0:
                message = f"Processing {work_done} of {total_work}"
                self.track_progress(message, work_done, total_work)

            time.sleep(sleep)

        if not self.has_cancelled():
            message = f"Processing {total_work} of {total_work}"
            self.track_progress(message, total_work, total_work)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My first window")

        button_width = 150
        button_height = 80

        self.__button_start = QPushButton("Start")
        self.__button_start.setFixedSize(button_width, button_height)
        self.__button_start.setStyleSheet("QPushButton { font-family: Century; font-size: 20pt; }")
        # noinspection PyUnresolvedReferences
        self.__button_start.clicked.connect(self.button_start_clicked)

        self.__button_pause = QPushButton("Pause")
        self.__button_pause.setFixedSize(button_width, button_height)
        self.__button_pause.setStyleSheet("QPushButton { font-family: Century; font-size: 20pt; }")
        # noinspection PyUnresolvedReferences
        self.__button_pause.clicked.connect(self.button_pause_clicked)

        self.__button_resume = QPushButton("Resume")
        self.__button_resume.setFixedSize(button_width, button_height)
        self.__button_resume.setStyleSheet("QPushButton { font-family: Century; font-size: 20pt; }")
        # noinspection PyUnresolvedReferences
        self.__button_resume.clicked.connect(self.button_resume_clicked)

        self.__button_cancel = QPushButton("Cancel")
        self.__button_cancel.setFixedSize(button_width, button_height)
        self.__button_cancel.setStyleSheet("QPushButton { font-family: Century; font-size: 20pt; }")
        # noinspection PyUnresolvedReferences
        self.__button_cancel.clicked.connect(self.button_cancel_clicked)

        widget = QWidget()
        hlayout = QHBoxLayout()
        hlayout.addStretch(1)
        hlayout.addWidget(self.__button_start, alignment=Qt.AlignmentFlag.AlignCenter)
        hlayout.addWidget(self.__button_pause, alignment=Qt.AlignmentFlag.AlignCenter)
        hlayout.addWidget(self.__button_resume, alignment=Qt.AlignmentFlag.AlignCenter)
        hlayout.addWidget(self.__button_cancel, alignment=Qt.AlignmentFlag.AlignCenter)
        hlayout.addStretch(1)
        vlayout = QVBoxLayout()
        vlayout.addLayout(hlayout)
        widget.setLayout(vlayout)
        self.setCentralWidget(widget)

        # Status bar
        self.__status_bar = QStatusBar()
        self.__status_bar.setStyleSheet("QStatusBar{border-top: 1px solid rgb(160,180,180);}")
        self.setStatusBar(self.__status_bar)

        self.__progress_bar = QProgressBar()
        self.__progress_bar.setFixedHeight(10)
        self.__progress_bar.setMaximumWidth(200)
        self.__progress_bar.setMaximum(100)

        self.__label_message = QLabel("")
        self.__label_state = QLabel("")

        self.__status_bar.addPermanentWidget(self.__label_message)
        self.__status_bar.addPermanentWidget(self.__label_state)
        self.__status_bar.addPermanentWidget(self.__progress_bar)


        self.__monitor: TaskMonitor or None = None
        self.__task: Task or None = None
        self.__timer = QTimer(self)

    def closeEvent(self, event: QEvent):
        if self.__task and not self.__task.has_finished():
            event.ignore()
            return
        event.accept()

    def button_start_clicked(self):
        if self.__task and not self.__task.has_finished():
            return
        print("button_start_clicked")

        self.__monitor = TaskMonitor()
        # noinspection PyUnresolvedReferences
        self.__timer.timeout.connect(self.timer_exec)

        self.__task = TaskTestMonitor(self.__monitor)
        thread = Thread(target=self.__task.executeTask)

        thread.start()
        self.__timer.start(50)

    def button_pause_clicked(self):
        if not self.__task.has_finished():
            self.__task.request_pause()

    def button_resume_clicked(self):
        if not self.__task.has_finished():
            self.__task.request_resume()

    def button_cancel_clicked(self):
        if self.__task:
            self.__task.request_cancel()

    def timer_exec(self):
        progress: TaskProgress = self.__monitor.get_progress()
        self.__label_message.setText(progress.message)
        self.__label_state.setText(progress.state.get_value)

        value = int(100 * progress.work_done / progress.total_work)
        self.__progress_bar.setValue(value)

        if progress.has_finished():
            self.__timer.disconnect()
            self.__timer.stop()



if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    msfx.lib.qt.setWidgetSize(window, 0.6, 0.6)
    window.show()
    sys.exit(app.exec())
