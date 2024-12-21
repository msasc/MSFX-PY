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
from typing import Tuple

from PyQt6.QtWidgets import QPushButton

class QPushButtonList:
    """
    Utility class to manage a list of QPushButton's.
    """
    def __init__(self):
        self.__buttons: list[QPushButton] = []

    def addButton(self, **kwargs):
        """
        Adds a button using the following keyword arguments.

        parameter kwargs options:
            - name (str): Name of the button, necessary to retrieve it.
            - text (str): Text of the button.
            - icon (QIcon): Optional icon for the button.
            - button (QPushButton): A button properly configured.
            - style (str): The style of the button
            - action (a function or method): Optional action to be executed.
            - action_kwargs (dict): Optional arguments.
            - any named properties.
        """
        std_args = ["name", "text", "icon", "button", "style", "action", "action_kwargs"]
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

        # The button style if passed as an argument.
        if kwargs.__contains__("style") and isinstance(kwargs["style"], str):
            button.setStyleSheet(kwargs["style"])

        # If an action has been passed, with optional arguments, connect it.
        if 'action' in kwargs and callable(kwargs['action']):
            action = kwargs.get("action")
            action_kwargs = kwargs.get("action_kwargs")
            # noinspection PyUnresolvedReferences
            button.clicked.connect(lambda: action(**action_kwargs))

        # Set any argument not contained in the list of standard arguments
        # as a property into the button.
        for key, value in kwargs.items():
            if key not in std_args:
                button.setProperty(key, value)

        # Add the button.
        self.__buttons.append(button)

    def getButton(self, name: str) -> QPushButton or None:
        """
        :param name: The object name of the button.
        :return: The button or None if not found.
        """
        for button in self.__buttons:
            if button.objectName() == name:
                return button
        return None

    def getButtonIndex(self, name: str) -> int:
        """
        :param name: The name of the button.
        :return: The index of the button or -1 if not found.
        """
        for i in range(len(self.__buttons)):
            if self.__buttons[i].objectName() == name:
                return i
        return -1

    def getButtons(self) -> Tuple[QPushButton, ...]:
        """
        :return: An immutable copy of the list of buttons.
        """
        return tuple(self.__buttons)

    def clearButtons(self):
        """
        Clear all buttons.
        """
        self.__buttons.clear()