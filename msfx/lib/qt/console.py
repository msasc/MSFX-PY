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

from PyQt6 import QtWidgets, QtGui
from datetime import datetime


class QConsole(QtWidgets.QWidget):
    """
    A logging console that publishes clear, log, print and println methods.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__cs = QtWidgets.QTextEdit()
        self.__cs.setLineWrapMode(QtWidgets.QTextEdit.LineWrapMode.NoWrap)
        font: QtGui.QFont = QtGui.QFont("Consolas", 10)
        self.__cs.setFont(font)
        policy = self.sizePolicy()
        policy.setHorizontalPolicy(QtWidgets.QSizePolicy.Policy.Maximum)
        policy.setVerticalPolicy(QtWidgets.QSizePolicy.Policy.Maximum)
        self.setSizePolicy(policy)

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.__cs)

    def print(self, text: str):
        """
        Prints text at the end of the current line.
        :param text: The text to print.
        """
        self.__cs.moveCursor(QtGui.QTextCursor.MoveOperation.End)
        self.__cs.insertPlainText(text)

    def println(self, text=None):
        """
        Prints text in a new line.
        :param text: The text to print or None.
        """
        self.__cs.append("")
        if not text is None:
            self.print(text)

    def log(self, text=None):
        """
        Logs the argument text in a new line preceded by a timestamp.
        :param text: The text to log.
        """
        if not text is None:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            text = now + "  " + text
            self.println(text)

    def clear(self):
        """
        Clears the current console content.
        """
        self.__cs.clear()
