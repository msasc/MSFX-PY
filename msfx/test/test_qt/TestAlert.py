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

from PyQt6.QtWidgets import (
    QApplication, QDialog, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy
)
from msfx.lib.qt import QBorderLayout
from msfx.lib.qt import setWidgetSize

class QAlert:
    def __init__(self):
        self.__dialog = QDialog()

        self.__layout = QBorderLayout()
        widget = QWidget()
        widget.setLayout(self.__layout)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.__dialog.setLayout(layout)
        layout.addWidget(widget)

        # List of buttons.
        self.__buttons = []

        # Name of the button clicked, returned by the show method when closed,
        # or accessed by the buttonClikedName method.
        self.__button_clicked_name = ""

        # Code, accept or cancel (rejected).
        self.__dialog_code = None

    def addButton(self, **kwargs):
        """
        Adds a button using the following keyword arguments.

        parameter kwargs options:
            - name (str): Name of the button, necessary to retrieve it.
            - text (str): Text of the button.
            - icon (QIcon): Optional icon for the button.
            - accept (bool): Whether the button will be an accept button and thus close the dialog settig the result to accept.
            - cancel (bool): Whether the button will be a cancel button and thus close the dialog settig the result to cancel or reject.
            - button (QPushButton): A button properly configured.
            - action (a function or method): Optional action to be executed.
            - action_kwargs (dict): Optional arguments.
        """

        button: QPushButton or None

        if kwargs.__contains__("button"):
            # The button has been passed as a parameter, must be a QPushButton
            if not isinstance(kwargs["button"], QPushButton):
                error = "Button must be a QPushButton"
                raise Exception(error)
            button: QPushButton = kwargs["button"]
            # The button must have a name to be able to retrieve it.
            if len(button.objectName()) == 0:
                error = f"Button '{button.text()}' must have a name"
                raise Exception(error)

        else:
            # To set a button, at least a name and a text is required.
            if not kwargs.__contains__("name"):
                raise Exception("A button must contain a name")
            name = kwargs["name"]
            text = ""
            if kwargs.__contains__("text"):
                text = kwargs["text"]
            button: QPushButton = QPushButton(text)
            button.setObjectName(name)

        # If an accept attribute is set, set it as aproperty.
        if kwargs.__contains__("accept") and kwargs.__contains__("cancel"):
            error = "A button can only be accept, cancel or none"
            raise Exception(error)

        if kwargs.__contains__("accept"):
            if isinstance(kwargs["accept"], bool):
                button.setProperty("accept", kwargs["accept"])
        if kwargs.__contains__("cancel"):
            if isinstance(kwargs["cancel"], bool):
                button.setProperty("cancel", kwargs["cancel"])

        # If an action has been passed, with optional arguments, connect it.
        if 'action' in kwargs and callable(kwargs['action']):
            action = kwargs.get("action")
            action_kwargs = kwargs.get("action_kwargs")
            button.clicked.connect(lambda: action(**action_kwargs))

        # Connect to __buttonClicked to manage actions.
        button.clicked.connect(lambda: self.__buttonClicked(button))
        self.__buttons.append(button)

    def show(self):
        # Bottom widget and layout to contain the buttons.
        bottom_widget = QWidget()
        bottom_layout = QHBoxLayout(bottom_widget)
        bottom_layout.setSpacing(2)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.addStretch(1)
        for button in self.__buttons:
            bottom_layout.addWidget(button)
        self.__layout.setBottom(bottom_widget)

        self.__dialog_code = self.__dialog.exec()
        return self.__button_clicked_name

    def getButtonClickedName(self):
        return self.__button_clicked_name

    def wasAccepted(self):
        return self.__dialog_code == QDialog.DialogCode.Accepted

    def wasCancelled(self):
        return self.__dialog_code == QDialog.DialogCode.Rejected

    def setSize(self, width_factor: float, height_factor: float):
        setWidgetSize(self.__dialog, width_factor, height_factor)

    def __buttonClicked(self, button: QPushButton):
        self.__button_clicked_name = button.objectName()
        # Check accept.
        if button.property("accept"):
            self.__dialog.accept()
        if button.property("cancel"):
            self.__dialog.reject()

def action_button(**kwargs):
    name = kwargs.get("name")
    age = kwargs.get("age")
    gender = kwargs.get("gender")
    print(f"Name: {name}, age: {age}, gender: {gender}")


if __name__ == "__main__":
    app = QApplication([])
    alert = QAlert()
    alert.setSize(0.5, 0.5)

    butt = QPushButton("Button 1")
    butt.setObjectName("B1")
    alert.addButton(button=butt, accept=True)

    butt = QPushButton("Button 2")
    butt.setObjectName("B2")
    alert.addButton(button=butt, accept=True, action=action_button, action_kwargs={'name': 'Michael', 'age': 50, 'gender': 'male'})

    alert.addButton(name="B3", text="Button 3", cancel=True)

    result = alert.show()
    print(result)
    print(alert.wasAccepted())
