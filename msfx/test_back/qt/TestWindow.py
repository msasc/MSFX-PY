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
import sys

from PyQt6.QtCore import (
    QObject, QThread, pyqtSignal
)
from PyQt6.QtGui import (
    QGuiApplication
)
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QStatusBar, QLabel, QProgressBar
)

import msfx.lib_back.qt

class Worker(QObject):
    # Signals to update and set visible or not, the status progress bar
    bar_progress = pyqtSignal(int)
    bar_visible = pyqtSignal(bool)

    # Signals to update and set visible or not, the status label
    label_text = pyqtSignal(str)
    label_visible = pyqtSignal(bool)

    def __init__(self, arg=None):
        super().__init__()

    def run(self):

        loops = 100
        sleep = 20

        QThread.msleep(1000)
        self.bar_visible.emit(True)
        for i in range(loops):
            self.bar_progress.emit(i + 1)  # Update progress bar
            QThread.msleep(sleep)  # Simulate a task that takes time
        QThread.msleep(1000)
        self.bar_visible.emit(False)

        QThread.msleep(1000)
        self.label_visible.emit(True)
        for i in range(loops):
            self.label_text.emit(f"Performing iteration {i+1} of current loop")  # Update progress bar
            QThread.msleep(sleep)  # Simulate a task that takes time
        QThread.msleep(1000)
        self.label_visible.emit(False)

        QThread.msleep(1000)
        self.label_visible.emit(True)
        self.bar_visible.emit(True)
        for i in range(loops):
            self.label_text.emit(f"Performing iteration {i+1} of current loop")  # Update progress bar
            self.bar_progress.emit(i + 1)  # Update progress bar
            QThread.msleep(sleep)  # Simulate a task that takes time
        self.bar_visible.emit(False)
        self.label_visible.emit(False)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My first window")

        # Set up the status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        # Add a standard message
        # self.statusBar.showMessage("Standard message")

        # Create a label and add it to the status bar
        self.statusLabel = QLabel("")
        # self.statusLabel.setFrameShape(QFrame.Shape.StyledPanel)

        # label_style = "QLabel { border: 0.5px solid gray; }"
        # self.statusLabel.setStyleSheet(label_style)


        # Create a progress bar and add it to the status bar
        self.progressBar = QProgressBar()
        self.progressBar.setFixedHeight(10)
        self.progressBar.setMaximumWidth(200)
        self.progressBar.setMaximum(100)  # Set the maximum value
        # self.progressBar.setValue(50)  # Set the current value

        self.statusBar.addPermanentWidget(self.statusLabel)  # This makes the label always visible
        self.statusBar.addPermanentWidget(self.progressBar)  # Add progress bar to the status bar

        self.statusLabel.setVisible(False)
        self.progressBar.setVisible(False)

        # Set up the thread and worker
        self.thread = QThread()
        self.worker = Worker(None)
        self.worker.moveToThread(self.thread)

        # Connect signals and slots
        self.worker.label_text.connect(self.statusLabel.setText)
        self.worker.label_visible.connect(self.statusLabel.setVisible)
        self.worker.bar_progress.connect(self.progressBar.setValue)
        self.worker.bar_visible.connect(self.progressBar.setVisible)

        # Start the thread
        self.thread.started.connect(self.worker.run)
        self.thread.start()

if __name__ == "__main__":
    app = QApplication([])
    screen = QGuiApplication.primaryScreen()

    window = Window()
    msfx.lib.qt.setWidgetSize(window, 0.6, 0.6)
    window.show()
    sys.exit(app.exec())