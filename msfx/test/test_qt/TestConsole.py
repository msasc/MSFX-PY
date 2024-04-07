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
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import QVBoxLayout
from msfx.lib.qt import QConsole

from msfx.lib import qt

from PyQt6.QtCore import QObject, QThread, pyqtSignal

class Worker(QObject):
    progress = pyqtSignal(str)  # Signal to write to the console

    def run(self):
        QThread.msleep(1000)
        n = 500
        for i in range(n+1):
            # Your time-consuming task here
            self.progress.emit(f"The number of the loop is {i}")  # Update progress bar
            QThread.msleep(1)  # Simulate a task that takes time


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My first window")

        self.cs = QConsole()
        layout = QVBoxLayout()
        layout.addWidget(self.cs)
        self.cs.setLayout(layout)

        self.setCentralWidget(self.cs)

        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)

        # Connect signals and slots
        self.worker.progress.connect(self.cs.log)
        self.thread.started.connect(self.worker.run)
        self.thread.start()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    screen = QtGui.QGuiApplication.primaryScreen()

    window = Window()
    qt.setWidgetSize(window, 0.6, 0.6)
    window.cs.log("Hola mamon")
    window.show()

    sys.exit(app.exec())
