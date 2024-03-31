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
import datetime
import sys

from PyQt6.QtCore import (
    QObject, QThread, pyqtSignal
)
from PyQt6.QtGui import (
    QGuiApplication
)
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QStatusBar, QLabel, QProgressBar, QWidget
)

from msfx.lib import qt

class Worker(QObject):

    # Signals to update and set visible or not, the status progress bar
    bar_progress = pyqtSignal(int)
    bar_visible = pyqtSignal(bool)

    # Signals to update and set visible or not, the status label
    label_text = pyqtSignal(str)
    label_visible = pyqtSignal(bool)

    # Signal to remove widgets
    remove_widget = pyqtSignal(QWidget)

    def __init__(self, status_bar: QStatusBar):
        super().__init__()
        self.status_bar = status_bar

        self.loops = 1000
        self.sleep = 1
        self.pause = 500

        # Create a progress bar and add it to the status bar
        self.statusLabel = QLabel("")
        self.progressBar = QProgressBar()
        self.progressBar.setFixedHeight(10)
        self.progressBar.setMaximumWidth(200)
        self.progressBar.setMaximum(self.loops)  # Set the maximum value
        # self.progressBar.setValue(50)  # Set the current value

        self.status_bar.addPermanentWidget(self.statusLabel)  # This makes the label always visible
        self.status_bar.addPermanentWidget(self.progressBar)  # Add progress bar to the status bar

        # Connect signals and slots
        self.label_text.connect(self.statusLabel.setText)
        self.label_visible.connect(self.statusLabel.setVisible)
        self.bar_progress.connect(self.progressBar.setValue)
        self.bar_visible.connect(self.progressBar.setVisible)
        self.remove_widget.connect(self.status_bar.removeWidget)

        self.statusLabel.setVisible(False)
        self.progressBar.setVisible(False)


    def run(self):

        QThread.msleep(self.pause)
        self.bar_visible.emit(True)

        # Pass 0, only progress bar.
        time_0_start = datetime.datetime.now()
        for i in range(self.loops):
            self.bar_progress.emit(i + 1)  # Update progress bar
            QThread.msleep(self.sleep)  # Simulate a task that takes time
        time_0_end = datetime.datetime.now()

        QThread.msleep(self.pause)
        self.bar_visible.emit(False)
        self.label_visible.emit(True)

        # Pass 1, only label.
        time_1_start = datetime.datetime.now()
        for i in range(self.loops):
            if i % 10 == 0:
                self.label_text.emit(f"Performing iteration {i} of current loop")  # Update progress bar
                QThread.msleep(self.sleep)  # Simulate a task that takes time
        self.label_text.emit(f"Performing iteration {self.loops} of current loop")  # Update progress bar
        time_1_end = datetime.datetime.now()

        QThread.msleep(self.pause)
        self.label_visible.emit(False)

        QThread.msleep(self.pause)
        self.label_visible.emit(True)
        self.bar_visible.emit(True)

        # Pass 2, label and progress bar.
        time_2_start = datetime.datetime.now()
        for i in range(self.loops):
            self.label_text.emit(f"Performing iteration {i+1} of current loop")  # Update progress bar
            self.bar_progress.emit(i + 1)  # Update progress bar
            QThread.msleep(self.sleep)  # Simulate a task that takes time
        time_2_end = datetime.datetime.now()

        QThread.msleep(self.pause)

        self.label_visible.emit(True)
        self.bar_visible.emit(False)

        text = f"{time_0_end-time_0_start}, {time_1_end-time_1_start}, {time_2_end-time_2_start}"
        self.label_text.emit(text)
        QThread.msleep(self.pause * 40)

        self.remove_widget.emit(self.progressBar)
        self.remove_widget.emit(self.statusLabel)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My first window")

        # Set up the status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        # Set up the thread and worker
        self.thread = QThread()
        self.worker = Worker(self.statusBar)
        self.worker.moveToThread(self.thread)

        # Start the thread
        self.thread.started.connect(self.worker.run)
        self.thread.start()

if __name__ == "__main__":
    app = QApplication([])
    screen = QGuiApplication.primaryScreen()
    window = Window()
    qt.setWidgetSize(window, 0.6, 0.6)
    window.show()
    sys.exit(app.exec())