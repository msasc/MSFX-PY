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
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import QTimer

class TimerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initialize_ui()

        # QTimer setup
        self.timer = QTimer(self)  # Create a QTimer instance
        self.timer.timeout.connect(self.update_label)  # Connect the timeout signal to the update_label method
        self.timer.start(100)  # Start the timer with a timeout interval of 1000 milliseconds (1 second)

    def initialize_ui(self):
        self.setWindowTitle('QTimer Example')
        self.setGeometry(100, 100, 250, 150)

        # QLabel setup
        self.label = QLabel('Counter: 0', self)
        self.label.move(50, 50)

        self.counter = 0

    def update_label(self):
        """Updates the label text."""
        self.counter += 1
        self.label.setText(f'Counter: {self.counter}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TimerWindow()
    window.show()
    sys.exit(app.exec())
