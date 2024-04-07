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

"""
Contains PyQT6 utility functions.

It is a formatting convention in Python that function or member names are in
lower case with words separated by an underscore. But in this qt module we
will follow the C++ convention that is used by all names in PyQt.
"""

from datetime import datetime

from PyQt6.QtCore import pyqtSignal, QSize
from PyQt6.QtGui import (
    QColor, QFont,
    QGuiApplication,
    QIconEngine, QIcon, QPen, QPainter, QPainterPath, QPixmap, QPaintEvent, QPalette,
    QTextCursor
)
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QTextEdit, QSizePolicy, QVBoxLayout, QHBoxLayout
)


def setWidgetSize(widget: QWidget, widthFactor: float, heightFactor: float):
    """
    Set the size of a widget relative to the primary screen size.
    :param widget: The widget to resize.
    :param widthFactor: The width factor to apply to the widget.
    :param heightFactor: The height factor to apply to the widget.
    :return: None
    """
    screenSize = QGuiApplication.primaryScreen().size()
    width = screenSize.width() * widthFactor
    height = screenSize.height() * heightFactor
    widget.resize(int(width), int(height))

class QCanvas(QWidget):
    """
    A canvas class.
    """
    # Define the paint signal.
    paint_canvas = pyqtSignal(QPaintEvent)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Pixmap with the last render when render mode is pixmap.
        self.__pixmap_previous: QPixmap = QPixmap(QSize())
        self.__pixmap_current: QPixmap = QPixmap(QSize())
        self.__pixel_ratio = QGuiApplication.primaryScreen().devicePixelRatio()

    def startPaint(self) -> QPainter:
        pixmap_size = self.size() * self.__pixel_ratio
        self.__pixmap_current = QPixmap(pixmap_size)
        self.__pixmap_current.setDevicePixelRatio(self.__pixel_ratio)
        self.__pixmap_current.fill(self.palette().color(QPalette.ColorRole.Base))
        painter: QPainter = QPainter(self.__pixmap_current)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        return painter

    def endPaint(self) -> None:
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.width(), self.height(), self.__pixmap_current)
        self.__pixmap_previous = self.__pixmap_current

    def paintEvent(self, event):
        """ Emits the paint signal. """
        super().paintEvent(event)
        self.paint_canvas.emit(event)


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
            self.hoverColor = QColor(240, 240, 240)
        if self.pressedColor is None:
            self.pressedColor = QColor(240, 240, 240)

        style = "QPushButton { background-color: " + self.backgroundColor.name() + "; } "
        style += "QPushButton:hover { background-color: " + self.hoverColor.name() + "; } "
        style += "QPushButton:pressed { background-color: " + self.pressedColor.name() + "; }"
        self.setStyleSheet(style)

        self.iconBase: QIconBase or None = None

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


class QConsole(QWidget):
    """
    A logging console that publishes clear, log, print and println methods.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__cs = QTextEdit()
        self.__cs.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        font: QFont = QFont("Consolas", 10)
        self.__cs.setFont(font)
        policy = self.sizePolicy()
        policy.setHorizontalPolicy(QSizePolicy.Policy.Maximum)
        policy.setVerticalPolicy(QSizePolicy.Policy.Maximum)
        self.setSizePolicy(policy)

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.__cs)

    def print(self, text: str):
        """
        Prints text at the end of the current line.
        :param text: The text to print.
        """
        self.__cs.moveCursor(QTextCursor.MoveOperation.End)
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


class QBorderLayout(QVBoxLayout):
    """
    A border layout with top, left, center, right and botton panes that expand
    according to the natura behavior of a border layout.
    """
    def __init__(self, parent=None, spacing=0):
        super(QBorderLayout, self).__init__(parent)

        # Top, left, center, right and bottom widgets.
        self.top = QWidget()
        self.left = QWidget()
        self.center = QWidget()
        self.right = QWidget()
        self.bottom = QWidget()

        # Main layout is a QVBoxLayout.
        self.setSpacing(spacing)

        # Add top widget.
        self.addWidget(self.top)

        # Center and Left/Right is a QHBoxLayout.
        self.centerLayout = QHBoxLayout()
        self.centerLayout.setSpacing(spacing)
        self.centerLayout.addWidget(self.left)
        self.center.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.centerLayout.addWidget(self.center)
        self.centerLayout.addWidget(self.right)
        self.addLayout(self.centerLayout)

        # Bottom
        self.addWidget(self.bottom)

    def setTop(self, top: QWidget or None):
        if top is None:
            top = QWidget()
        if self.top:
            self.removeWidget(self.top)
            self.top.deleteLater()
        top.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred))
        self.insertWidget(0, top)
        self.top = top

    def setLeft(self, left: QWidget or None):
        if left is None:
            left = QWidget()
        if self.left:
            self.centerLayout.removeWidget(self.left)
            self.left.deleteLater()
        left.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding))
        self.centerLayout.insertWidget(0, left)
        self.left = left

    def setCenter(self, center: QWidget or None):
        if center is None:
            center = QWidget()
        if self.center:
            self.centerLayout.removeWidget(self.center)
            self.center.deleteLater()
        center.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.centerLayout.insertWidget(1, center)
        self.center = center

    def setRight(self, right: QWidget or None):
        if right is None:
            right = QWidget()
        if self.right:
            self.centerLayout.removeWidget(self.right)
            self.right.deleteLater()
        right.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding))
        self.centerLayout.insertWidget(2, right)
        self.right = right

    def setBottom(self, bottom: QWidget or None):
        if bottom is None:
            bottom = QWidget()
        if self.bottom:
            self.removeWidget(self.bottom)
            self.bottom.deleteLater()
        bottom.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred))
        self.insertWidget(2, bottom)
        self.bottom = bottom
