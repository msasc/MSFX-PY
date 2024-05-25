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
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QStyle, QLabel, QTextBrowser

from msfx.lib.qt import setWidgetSize
from msfx.lib.qt.pane import QBorderPane, QHBoxPane
from msfx.lib.qt.button_list import QPushButtonList

class QAlert:
    def __init__(self):
        self.__dialog = QDialog()
        self.__borderPane = QBorderPane()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.__borderPane)
        self.__dialog.setLayout(layout)

        # Type: plain, warning, question, error
        self.__type = "plain"

        # List of buttons.
        self.__buttons = QPushButtonList()

        # Name of the button clicked, returned by the show method when closed,
        # or accessed by the buttonClikedName method.
        self.__button_clicked_name = ""

        # Code, accept or cancel (rejected).
        self.__dialog_code = None

        # Central widget, normally none and will show a text, but can be any widget.
        self.__central_widget: QWidget or None = None

        # Normal/HTML text to be shown in the center.
        self.__text = None

        # Normal/HTML text to be shown as the title.
        self.__title = None
        self.__title_style = None

    def addButton(self, **kwargs):
        self.__buttons.addButton(**kwargs)

        # Connect the added button to __buttonClicked to manage actions.
        button = self.__buttons.getButtons()[len(self.__buttons.getButtons()) - 1]
        button.clicked.connect(lambda: self.__buttonClicked(button))

    def setCentralWidget(self, widget: QWidget):
        self.__central_widget = widget
        self.__text = None

    def setText(self, text):
        if text is not None and not isinstance(text, str):
            raise Exception("Text must be a string")
        self.__text = text
        self.__central_widget = None

    def setTitle(self, title, style=None):
        if title is not None and not isinstance(title, str):
            raise Exception("Title must be a string")
        if style is not None and not isinstance(style, str):
            raise Exception("Style must be a string")
        self.__title = title
        self.__title_style = style

    def setTypeError(self):
        self.__type = "error"

    def setTypeInformation(self):
        self.__type = "information"

    def setTypePlain(self):
        self.__type = "plain"

    def setTypeQuestion(self):
        self.__type = "question"

    def setTypeWarning(self):
        self.__type = "warning"

    def show(self):
        size = QPushButton().sizeHint().height()
        for button in self.__buttons.getButtons():
            size = max(size, button.sizeHint().height())

        # Top title.
        if self.__title is not None:
            titleLabel = QLabel()
            titleLabel.setText(self.__title)
            if self.__title_style is not None:
                titleLabel.setStyleSheet("QLabel { " + self.__title_style + "}")
            self.__borderPane.layout().setTop(titleLabel)

        # Central widget is a text.
        if self.__text is not None:
            textBrowser = QTextBrowser()
            textBrowser.setHtml(self.__text)
            self.__borderPane.layout().setCenter(textBrowser)

        # Central widget is any widget.
        if self.__central_widget is not None:
            self.__borderPane.layout().setCenter(self.__central_widget)

        # Bottom widget and layout to contain the buttons.
        bottom_pane = QHBoxPane()
        bottom_pane.layout().setSpacing(2)
        bottom_pane.layout().setContentsMargins(0, 5, 0, 0)

        icon: QIcon or None = None
        if self.__type == "error":
            icon = self.__dialog.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxCritical)
        if self.__type == "information":
            icon = self.__dialog.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation)
        if self.__type == "question":
            icon = self.__dialog.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxQuestion)
        if self.__type == "warning":
            icon = self.__dialog.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxWarning)
        labelIcon = QLabel()
        labelIcon.setPixmap(icon.pixmap(size, size))
        bottom_pane.layout().addWidget(labelIcon, 1, Qt.AlignmentFlag.AlignLeft)

        bottom_pane.layout().addStretch(1)
        for button in self.__buttons.getButtons():
            bottom_pane.layout().addWidget(button)
        self.__borderPane.layout().setBottom(bottom_pane)

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
