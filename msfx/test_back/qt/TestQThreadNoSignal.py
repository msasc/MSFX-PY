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

from PyQt6.QtCore import QObject, QThread
from PyQt6.QtWidgets import QApplication, QMainWindow, QProgressBar

import msfx.lib_back2.qt

class Worker(QObject):
    def __init__(self, progressBar: QProgressBar):
        super().__init__(None)
        self.progressBar = progressBar

    def run(self):
        # self.progressBar.setValue(1000)
        # QThread.msleep(1)
        for i in range(10):
            # Your time-consuming task here
            self.progressBar.setValue(i + 1)  # Update progress bar
            QThread.sleep(1)  # Simulate a task that takes time

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.progressBar = QProgressBar(self)

        # Initialize the progress bar and other UI components
        self.progressBar.setGeometry(30, 40, 200, 16)
        self.progressBar.setMaximum(10)
        self.progressBar.setTextVisible(True)

        # Set up the thread and worker
        self.thread = QThread()
        self.worker = Worker(self.progressBar)
        self.worker.moveToThread(self.thread)

        # Start the thread
        # noinspection PyUnresolvedReferences
        self.thread.started.connect(self.worker.run)
        self.thread.start()

app = QApplication(sys.argv)
window = MainWindow()
msfx.lib.qt.setWidgetSize(window, 0.4, 0.3)
window.show()
sys.exit(app.exec())
