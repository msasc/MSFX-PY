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
    QWidget, QBoxLayout, QHBoxLayout, QVBoxLayout, QSizePolicy
)
from PyQt6.QtCore import (
    QMargins
)

class QBorderLayout(QWidget):
    def __init__(self):
        super().__init__()

        # Top, left, center, right and bottom widgets.
        self.top = QWidget()
        self.left = QWidget()
        self.center = QWidget()
        self.right = QWidget()
        self.bottom = QWidget()

        # Main layout is a QVBoxLayout.
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setSpacing(0)

        # Add top widget.
        self.mainLayout.addWidget(self.top)

        # Center and Left/Right is a QHBoxLayout.
        self.centerLayout = QHBoxLayout()
        self.centerLayout.setSpacing(0)
        self.centerLayout.addWidget(self.left)
        self.center.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.centerLayout.addWidget(self.center)
        self.centerLayout.addWidget(self.right)
        self.mainLayout.addLayout(self.centerLayout)

        # Bottom
        self.mainLayout.addWidget(self.bottom)

    def __replaceWidget(
        self,
        layout: QBoxLayout,
        position: int,
        oldWidget: QWidget,
        newWidget: QWidget,
        horzPolicy: QSizePolicy.Policy,
        vertPolicy: QSizePolicy.Policy,
        margins: QMargins = QMargins(0, 0, 0, 0)):
        if newWidget is None:
            newWidget = QWidget()

        if oldWidget:
            layout.removeWidget(oldWidget)
            oldWidget.deleteLater()

        newWidget.setSizePolicy(horzPolicy, vertPolicy)

        container = QWidget()
        containerLayout = QVBoxLayout(container)
        containerLayout.setContentsMargins(margins)
        containerLayout.setSpacing(0)
        containerLayout.addWidget(newWidget)
        container.setSizePolicy(horzPolicy, vertPolicy)

        layout.insertWidget(position, container)

    def setTop(self, top: QWidget or None, margins: QMargins = QMargins(0, 0, 0, 0)):
        self.__replaceWidget(
            self.mainLayout,
            0,
            self.top,
            top,
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
            margins)

    def setLeft(self, left: QWidget or None, margins: QMargins = QMargins(0, 0, 0, 0)):
        self.__replaceWidget(
            self.centerLayout,
            0,
            self.left,
            left,
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding,
            margins)

    def setCenter(self, center: QWidget or None, margins: QMargins = QMargins(0, 0, 0, 0)):
        self.__replaceWidget(
            self.centerLayout,
            1,
            self.center,
            center,
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
            margins)

    def setRight(self, right: QWidget or None, margins: QMargins = QMargins(0, 0, 0, 0)):
        self.__replaceWidget(
            self.centerLayout,
            2,
            self.right,
            right,
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding,
            margins)

    def setBottom(self, bottom: QWidget or None, margins: QMargins = QMargins(0, 0, 0, 0)):
        self.__replaceWidget(
            self.mainLayout,
            2,
            self.bottom,
            bottom,
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
            margins)
