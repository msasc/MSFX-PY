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

from PyQt6.QtCore import Qt, QMargins
from PyQt6.QtWidgets import (
    QApplication, QPushButton, QLabel, QWidget, QVBoxLayout, QSizePolicy
)
from msfx.lib.qt.layout import QBorderLayout

def get_widget(widget: QWidget, margins=(0, 0, 0, 0)) -> QWidget:
    container = QWidget()
    containerLayout = QVBoxLayout(container)
    containerLayout.setContentsMargins(*margins)
    containerLayout.setSpacing(0)
    containerLayout.addWidget(widget)
    widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    return container

if __name__ == '__main__':
    app = QApplication([])
    wnd = QBorderLayout()
    wnd.setTop(QPushButton("Top"))
    wnd.setLeft(QPushButton("Left"))
    wnd.setCenter(QPushButton("Center"))
    wnd.setRight(QPushButton("Right"))
    wnd.setBottom(QPushButton("Bottom"))
    # wnd.setTop(QPushButton("Top"), QMargins(2, 2, 2, 2))
    # wnd.setLeft(QPushButton("Left"), QMargins(2, 2, 2, 2))
    # wnd.setCenter(QPushButton("Center"), QMargins(2, 2, 2, 2))
    # wnd.setRight(QPushButton("Right"), QMargins(2, 2, 2, 2))
    # wnd.setBottom(QPushButton("Bottom"), QMargins(2, 2, 2, 2))
    wnd.show()
    app.exec()
