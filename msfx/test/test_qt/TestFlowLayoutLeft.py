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

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLayout, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import QRect, QSize, QPoint, Qt

class QFlowLayout(QLayout):
    def __init__(self, spacing=0):
        super(QFlowLayout, self).__init__()
        self.setSpacing(spacing)
        self.itemList = []

    def addItem(self, item):
        self.itemList.append(item)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()

        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        size += QSize(2 * self.spacing(), 2 * self.spacing())
        return size

    def setGeometry(self, rect):
        super(QFlowLayout, self).setGeometry(rect)

        if self.itemList:
            x = rect.x()
            y = rect.y()
            lineHeight = 0

            for item in self.itemList:
                wid = item.widget()
                spaceX = self.spacing() + wid.style().layoutSpacing(QSizePolicy.ControlType.PushButton, QSizePolicy.ControlType.PushButton, Qt.Orientation.Horizontal)
                spaceY = self.spacing() + wid.style().layoutSpacing(QSizePolicy.ControlType.PushButton, QSizePolicy.ControlType.PushButton, Qt.Orientation.Vertical)
                nextX = x + item.sizeHint().width() + spaceX
                if nextX - spaceX > rect.right() and lineHeight > 0:
                    x = rect.x()
                    y = y + lineHeight + spaceY
                    nextX = x + item.sizeHint().width() + spaceX
                    lineHeight = 0

                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

                x = nextX
                lineHeight = max(lineHeight, item.sizeHint().height())

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList.pop(index)
        return None

# Example usage
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        flowLayout = QFlowLayout(spacing=2)
        buttons = [QPushButton(f"Button {i}") for i in range(10)]
        for button in buttons:
            flowLayout.addWidget(button)

        layout.addLayout(flowLayout)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
