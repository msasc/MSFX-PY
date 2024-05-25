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

from PyQt6.QtCore import pyqtSignal, QSize
from PyQt6.QtGui import QPainter, QPixmap, QGuiApplication, QPaintEvent, QPalette
from PyQt6.QtWidgets import QWidget

class QCanvas(QWidget):
    """
    A canvas class.
    """
    # Define the paint signal.
    paintCanvas = pyqtSignal(QPaintEvent)

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
        self.paintCanvas.emit(event)
