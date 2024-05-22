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
from PyQt6.QtGui import QIconEngine, QColor, QPen, QPainterPath, QIcon
from PyQt6.QtWidgets import QPushButton


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

        self.backgroundColor = backgroundColor
        self.hoverColor = hoverColor
        self.pressedColor = pressedColor

        if self.backgroundColor is None:
            self.backgroundColor = QColor(240, 240, 240)
        if self.hoverColor is None:
            self.hoverColor = QColor(230, 230, 230)
        if self.pressedColor is None:
            self.pressedColor = QColor(220, 215, 215)

        style = "QPushButton { background-color: " + self.backgroundColor.name() + "; } "
        style += "QPushButton:hover { background-color: " + self.hoverColor.name() + "; } "
        style += "QPushButton:pressed { background-color: " + self.pressedColor.name() + "; }"
        self.setStyleSheet(style)

        self.iconBase: QIconBase or None = None
        self.isPressed: bool = False

    def setIconBase(self, iconBase: QIconBase):
        self.iconBase = iconBase
        self.iconBase.setBackgroundColor(self.backgroundColor)
        self.setIcon(QIcon(self.iconBase))

    def enterEvent(self, event):
        self.iconBase.setBackgroundColor(self.hoverColor)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.iconBase.setBackgroundColor(self.backgroundColor)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.iconBase.setBackgroundColor(self.pressedColor)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.iconBase.setBackgroundColor(self.hoverColor)
        super().mouseReleaseEvent(event)


