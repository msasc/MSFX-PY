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

import sys

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout

from msfx.lib_back2.qt.icon import QIconClose, QIconButton


# Do run the app.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    button = QIconButton()
    button.setFixedSize(QSize(120, 120))
    button.setIconSize(QSize(60, 60))
    button.setIconBase(QIconClose())

    layout = QGridLayout()
    layout.addWidget(button, 1, 1, 1, 1)
    layout.setRowStretch(0, 1)
    layout.setRowStretch(2, 1)
    layout.setColumnStretch(0, 1)
    layout.setColumnStretch(2, 1)

    window = QWidget()
    window.setLayout(layout)
    window.show()

    sys.exit(app.exec())
