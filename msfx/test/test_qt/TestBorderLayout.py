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

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from msfx.lib.qt import setWidgetSize
from msfx.lib.qt.layout import QBorderLayout

if __name__ == '__main__':
    app = QApplication([])
    wnd = QMainWindow()
    widget = QWidget()
    layout = QBorderLayout(parent=widget)
    layout.setTop(QPushButton("Top"))
    layout.setTop(QPushButton("Top after"))
    layout.setLeft(QPushButton("Left"))
    layout.setCenter(QPushButton("Center"))
    layout.setCenter(QPushButton("Center after"))
    layout.setRight(QPushButton("Right"))
    layout.setBottom(QPushButton("Bottom"))
    # widget.setLayout(layout)
    wnd.setCentralWidget(widget)

    setWidgetSize(wnd, 0.6, 0.6)
    wnd.show()
    app.exec()
