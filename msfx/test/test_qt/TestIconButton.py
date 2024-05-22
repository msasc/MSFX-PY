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

from PyQt6.QtGui import QIconEngine, QColor, QIcon, QPen, QPainterPath, QCursor, QPalette
from PyQt6.QtWidgets import QApplication, QPushButton, QWidget, QGridLayout
from PyQt6.QtCore import QSize

class QIconBase(QIconEngine):

    def __init__(self, backgroundColor: QColor = None):
        super().__init__()
        self.backgroundColor = backgroundColor
        if self.backgroundColor is None:
            self.backgroundColor = QColor(240, 240, 240)

    def setBackgroundColor(self, backgroundColor: QColor):
        if not backgroundColor is None:
            self.backgroundColor = backgroundColor

    def paint(self, painter, rect, mode, state):
        painter.fillRect(rect, self.backgroundColor)

    def clone(self):
        return QIconBase(self.backgroundColor)

class QIconClose(QIconBase):
    def __init__(self, backgroundColor: QColor = None):
        super().__init__(backgroundColor)

    def paint(self, painter, rect, mode, state):
        super().paint(painter, rect, mode, state)
        pen = QPen(QColor(20, 20, 20))
        pen.setWidth(2)
        painter.setPen(pen)
        path = QPainterPath()
        path.moveTo(rect.topLeft().x(), rect.topLeft().y())
        path.lineTo(rect.bottomRight().x(), rect.bottomRight().y())
        path.moveTo(rect.topRight().x(), rect.topRight().y())
        path.lineTo(rect.bottomLeft().x(), rect.bottomLeft().y())
        painter.drawPath(path)

class QIconButton(QPushButton):
    def __init__(self, backgroundColor: QColor = None, hoverColor: QColor = None, pressedColor: QColor = None):
        super().__init__()

        self.__backgroundColor = backgroundColor
        self.__hoverColor = hoverColor
        self.__pressedColor = pressedColor

        if self.__backgroundColor is None:
            self.__backgroundColor = QColor(240, 240, 240)
        if self.__hoverColor is None:
            self.__hoverColor = QColor(230, 230, 230)
        if self.__pressedColor is None:
            self.__pressedColor = QColor(220, 215, 215)

        style = "QPushButton { background-color: " + self.__backgroundColor.name() + "; } "
        style += "QPushButton:hover { background-color: " + self.__hoverColor.name() + "; } "
        style += "QPushButton:pressed { background-color: " + self.__pressedColor.name() + "; }"
        self.setStyleSheet(style)

        self.__iconBase: QIconBase or None = None
        self.__entered = False
        self.__pressed = False

    def __updateIconBaseColor(self):
        color: QColor = self.__backgroundColor
        if self.__entered:
            if self.__pressed:
                color = self.__pressedColor
            else:
                color = self.__hoverColor
        else:
            color = self.__backgroundColor
        self.__iconBase.setBackgroundColor(color)
        self.update()


    def setIconBase(self, iconBase: QIconBase):
        self.__iconBase = iconBase
        self.__iconBase.setBackgroundColor(self.__backgroundColor)
        self.setIcon(QIcon(self.__iconBase))

    def enterEvent(self, event):
        self.__entered = True
        self.__updateIconBaseColor()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.__entered = False
        self.__updateIconBaseColor()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.__pressed = True
        self.__updateIconBaseColor()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.__entered = self.rect().contains(self.mapFromGlobal(QCursor.pos()))
        self.__updateIconBaseColor()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.__pressed = False
        self.__updateIconBaseColor()
        super().mouseReleaseEvent(event)


# Do run the app.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    button = QIconButton()
    button.setFixedSize(QSize(120, 120))
    button.setIconSize(QSize(60, 60))
    button.setIconBase(QIconClose())

    layout = QGridLayout()
    layout.addWidget(button, 1, 1, 1, 1)
    layout.setRowStretch(0, 1)
    layout.setRowStretch(2, 1)
    layout.setColumnStretch(0, 1)
    layout.setColumnStretch(2, 1)

    window = QWidget()
    window.setLayout(layout)
    window.show()

    sys.exit(app.exec())
