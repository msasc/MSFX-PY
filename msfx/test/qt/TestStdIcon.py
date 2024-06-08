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

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QStyle

# QMessageBox.information(None, "Information", "This is an informational message.")
# QMessageBox.warning(None, "Warning", "This is a warning message.")
# QMessageBox.critical(None, "Error", "This is an error message.")
# QMessageBox.question(None, "Question", "Are you sure?")

app = QApplication([])
window = QMainWindow()
window.setWindowTitle('Standard Icons Example')
window.setGeometry(100, 100, 300, 200)

# Create a button and set a standard icon
button = QPushButton(window)
icon = window.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxQuestion)
button.setIcon(icon)
button.setText("Question")
button.setStyleSheet("QPushButton { sub-control: padding: 30px; }")
button.show()

window.show()
app.exec()
