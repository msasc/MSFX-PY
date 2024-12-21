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
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QSizePolicy, QWidget, QVBoxLayout, QHBoxLayout, QLabel

from msfx.lib_back2.qt import getBackgroundColor, setBackgroundColor


class QBorderLayout(QVBoxLayout):
    """
    A border layout with top, left, center, right and botton panes that expand
    according to the natura behavior of a border layout.
    """
    def __init__(self, parent=None, spacing=0):
        super(QBorderLayout, self).__init__(parent)

        # Top, left, center, right and bottom widgets.
        self.__top = QWidget()
        self.__left = QWidget()
        self.__center = QWidget()
        self.__right = QWidget()
        self.__bottom = QWidget()

        # Main layout is a QVBoxLayout.
        self.setSpacing(spacing)

        # Add top widget.
        self.addWidget(self.__top)

        # Center and Left/Right is a QHBoxLayout.
        self.centerLayout = QHBoxLayout()
        self.centerLayout.setSpacing(spacing)
        self.centerLayout.addWidget(self.__left)
        self.__center.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.centerLayout.addWidget(self.__center)
        self.centerLayout.addWidget(self.__right)
        self.addLayout(self.centerLayout)

        # Bottom
        self.addWidget(self.__bottom)

    def setTop(self, top: QWidget or None):
        if top is None:
            top = QWidget()
        if self.__top:
            self.removeWidget(self.__top)
            self.__top.deleteLater()
        top.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred))
        self.insertWidget(0, top)
        self.__top = top

    def setLeft(self, left: QWidget or None):
        if left is None:
            left = QWidget()
        if self.__left:
            self.centerLayout.removeWidget(self.__left)
            self.__left.deleteLater()
        left.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding))
        self.centerLayout.insertWidget(0, left)
        self.__left = left

    def setCenter(self, center: QWidget or None):
        if center is None:
            center = QWidget()
        if self.__center:
            self.centerLayout.removeWidget(self.__center)
            self.__center.deleteLater()
        center.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.centerLayout.insertWidget(1, center)
        self.__center = center

    def setRight(self, right: QWidget or None):
        if right is None:
            right = QWidget()
        if self.__right:
            self.centerLayout.removeWidget(self.__right)
            self.__right.deleteLater()
        right.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding))
        self.centerLayout.insertWidget(2, right)
        self.__right = right

    def setBottom(self, bottom: QWidget or None):
        if bottom is None:
            bottom = QWidget()
        if self.__bottom:
            self.removeWidget(self.__bottom)
            self.__bottom.deleteLater()
        bottom.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred))
        self.insertWidget(2, bottom)
        self.__bottom = bottom

    def setBackgroundColor(self, color: QColor):
        if color is None:
            raise Exception("Background color can not be None")
        color: QColor = getBackgroundColor(QLabel())
        setBackgroundColor(self.__top, color)
        setBackgroundColor(self.__left, color)
        setBackgroundColor(self.__right, color)
        setBackgroundColor(self.__bottom, color)
        setBackgroundColor(self.__center, color)