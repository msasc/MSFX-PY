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
    QApplication, QMainWindow, QStatusBar, QLabel, QProgressBar, QFrame, QWidget
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

        # Create a progress bar and add it to the status bar
        self.statusLabel = QLabel("")
        self.progressBar = QProgressBar()
        self.progressBar.setFixedHeight(10)
        self.progressBar.setMaximumWidth(200)
        self.progressBar.setMaximum(100)  # Set the maximum value
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

        loops = 100
        sleep = 10
        pause = 1000

        QThread.msleep(pause)
        self.bar_visible.emit(True)
        for i in range(loops):
            self.bar_progress.emit(i + 1)  # Update progress bar
            QThread.msleep(sleep)  # Simulate a task that takes time
        QThread.msleep(pause)
        self.bar_visible.emit(False)

        QThread.msleep(pause)
        self.label_visible.emit(True)
        for i in range(loops):
            self.label_text.emit(f"Performing iteration {i+1} of current loop")  # Update progress bar
            QThread.msleep(sleep)  # Simulate a task that takes time
        QThread.msleep(pause)
        self.label_visible.emit(False)

        QThread.msleep(pause)
        self.label_visible.emit(True)
        self.bar_visible.emit(True)
        for i in range(loops):
            self.label_text.emit(f"Performing iteration {i+1} of current loop")  # Update progress bar
            self.bar_progress.emit(i + 1)  # Update progress bar
            QThread.msleep(sleep)  # Simulate a task that takes time

        QThread.msleep(pause)

        self.remove_widget.emit(self.progressBar)
        self.label_text.emit("This is the final text after ending iterations")
        QThread.msleep(pause * 2)
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
    qt.set_size(window, 0.6, 0.6)
    window.show()
    sys.exit(app.exec())