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

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy

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
