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
    # Alignment options
    AlignLeft = 0
    AlignRight = 1

    def __init__(self, parent=None, margin=0, spacing=-1, alignment=AlignLeft):
        super().__init__(parent)

        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)

        self.setSpacing(spacing)
        self.itemList = []
        self.alignment = alignment

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

        if not self.itemList:
            return

        rightOffset = rect.right()
        currentRowWidth = 0
        currentRowItems = []
        lineHeight = 0

        for item in self.itemList:
            itemWidth = item.sizeHint().width() + self.spacing()
            itemHeight = item.sizeHint().height() + self.spacing()
            lineHeight = max(lineHeight, itemHeight)

            if self.alignment == self.AlignLeft:
                nextX = currentRowWidth + itemWidth
                if nextX - self.spacing() > rect.width():  # Wrap to next line
                    currentRowWidth = 0
                    rightOffset = rect.y() + lineHeight

                item.setGeometry(QRect(QPoint(currentRowWidth, rightOffset), item.sizeHint()))
                currentRowWidth += itemWidth

            else:  # AlignRight
                if currentRowWidth + itemWidth > rect.width():
                    rightOffset -= currentRowWidth  # Adjust starting point for the previous row
                    for rowItem, xShift in reversed(currentRowItems):
                        newY = rowItem.geometry().y() if currentRowItems else rect.y()
                        rowItem.setGeometry(QRect(QPoint(rightOffset + xShift, newY), rowItem.sizeHint()))
                    currentRowWidth = 0
                    currentRowItems.clear()
                    rightOffset = rect.right()
                currentRowItems.append((item, currentRowWidth))
                currentRowWidth += itemWidth

        # For AlignRight, align the last row of items
        if self.alignment == self.AlignRight:
            rightOffset -= currentRowWidth
            for rowItem, xShift in reversed(currentRowItems):
                newY = rowItem.geometry().y() if currentRowItems else rect.y()
                rowItem.setGeometry(QRect(QPoint(rightOffset + xShift, newY), rowItem.sizeHint()))

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
        self.setWindowTitle("Flow Layout Example - Aligned")
        layout = QVBoxLayout(self)

        # Create a flow layout with right alignment
        flowLayout = QFlowLayout(alignment=QFlowLayout.AlignLeft)
        buttons = [QPushButton(f"Button {i}") for i in range(10)]
        for button in buttons:
            flowLayout.addWidget(button)

        layout.addLayout(flowLayout)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.resize(400, 200)  # Optional: to see the wrapping behavior on startup
    window.show()
    app.exec()
