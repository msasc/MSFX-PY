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
from PyQt6.QtWidgets import QWidget, QHBoxLayout

from msfx.lib_back.qt.layout import QBorderLayout

class QBorderPane(QWidget):
    def __init__(self):
        super().__init__()
        self.__layout = QBorderLayout()
        self.setLayout(self.__layout)
    def layout(self) -> QBorderLayout:
        return self.__layout

class QHBoxPane(QWidget):
    def __init__(self):
        super().__init__()
        self.__layout = QHBoxLayout()
        self.setLayout(self.__layout)
    def layout(self) -> QHBoxLayout:
        return self.__layout