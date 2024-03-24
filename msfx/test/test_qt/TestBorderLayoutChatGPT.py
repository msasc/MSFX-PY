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
from PyQt6.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout,
                             QPushButton, QSizePolicy)

class BorderLayout(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout
        mainLayout = QVBoxLayout(self)

        # North
        northBtn = QPushButton("North")
        mainLayout.addWidget(northBtn)

        # Center and East/West
        centerLayout = QHBoxLayout()

        westBtn = QPushButton("West")
        centerLayout.addWidget(westBtn)

        centerBtn = QPushButton("Center")
        centerBtn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        centerLayout.addWidget(centerBtn)

        eastBtn = QPushButton("East")
        centerLayout.addWidget(eastBtn)

        mainLayout.addLayout(centerLayout)

        # South
        southBtn = QPushButton("South")
        mainLayout.addWidget(southBtn)

if __name__ == '__main__':
    app = QApplication([])
    window = BorderLayout()
    window.show()
    app.exec()
