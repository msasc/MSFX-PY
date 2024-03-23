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

from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton

class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Custom Dialog with Multiple Buttons")
        self.userChoice = None  # Variable to store the user's choice

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Button 1
        btn1 = QPushButton("Option 1")
        btn1.clicked.connect(lambda: self.buttonClicked("Option 1", True))
        layout.addWidget(btn1)

        # Button 2
        btn2 = QPushButton("Option 2")
        btn2.clicked.connect(lambda: self.buttonClicked("Option 2", True))
        layout.addWidget(btn2)

        # Button 3
        btn3 = QPushButton("Option 3")
        btn3.clicked.connect(lambda: self.buttonClicked("Option 3", False))
        layout.addWidget(btn3)

    def buttonClicked(self, choice: str, accept: bool):
        """Slot to handle button clicks."""
        self.userChoice = choice  # Set the user's choice
        if accept:
            self.accept()
        else:
            self.reject()

# Example usage
app = QApplication([])
dialog = CustomDialog()
cancel: bool = (dialog.exec() == QDialog.DialogCode.Rejected)
print(f"User selected: {dialog.userChoice}, Cancelled: {cancel}")
