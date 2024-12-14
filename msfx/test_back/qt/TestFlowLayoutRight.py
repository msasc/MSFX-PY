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
    def __init__(self, parent=None, margin=0, spacing=-1):
        super(QFlowLayout, self).__init__(parent)

        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)

        self.spacing = spacing
        self.itemList = []

    def addItem(self, item):
        # self.itemList.insert(0, item)
        self.itemList.append(item)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())
        size += QSize(2 * self.spacing, 2 * self.spacing)
        return size

    def setGeometry(self, rect):
        super(QFlowLayout, self).setGeometry(rect)
        if not self.itemList:
            return

        x, y, lineHeight = rect.width(), 0, 0
        for item in reversed(self.itemList):
            spaceX = self.spacing + item.widget().style().layoutSpacing(QSizePolicy.ControlType.PushButton,
                                                                        QSizePolicy.ControlType.PushButton,
                                                                        Qt.Orientation.Horizontal)
            nextX = x - item.sizeHint().width() - spaceX
            if nextX < 0:
                x = rect.width()
                y = y + lineHeight + spaceX
                lineHeight = 0
                nextX = x - item.sizeHint().width() - spaceX

            item.setGeometry(QRect(QPoint(nextX, y), item.sizeHint()))
            x = nextX - spaceX
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
        self.setWindowTitle("Right Aligned Flow Layout")
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QWidget())  # Placeholder for other content

        flowLayout = QFlowLayout()
        for i in range(10):
            flowLayout.addWidget(QPushButton(f"Button {i}"))
        container = QWidget()
        container.setLayout(flowLayout)
        self.layout().addWidget(container)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
