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

"""
Application in charge of managing market data, drawing charts, generating
sequences of images to test reinforcement algorithms, and many more.
"""

# Python language imports.
import sys

# PyQt6 imports.
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QStatusBar,
    QTabWidget,
    QWidget,
    QTabBar
)

# msfx imports.
from msfx.lib import qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Market Data Manager")

        # Set up the status bar. The status bar can be accessed by any process,
        # and connecting signals widgets can be added, updated and removed.
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready", 5000)

        # Central widget is a tab pane.
        self.tabPane = QTabWidget()
        self.tabPane.setTabsClosable(True)
        self.setCentralWidget(self.tabPane)

        # First tab contains a console that will be unique within the
        # application and that can be accessed by any process to connect
        # signals and log messages.
        self.console = qt.QConsole()
        self.console.setProperty("key", "console")
        self.addTab(self.console, "Console", False)

    def addTab(self, widget, title, closeable=True):
        self.tabPane.addTab(widget, title)
        index = self.tabPane.count() - 1
        if not closeable:
            tab_bar = self.tabPane.tabBar()
            tab_bar.setTabButton(index, QTabBar.ButtonPosition.RightSide, None)

# Do run the app.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    wnd = MainWindow()
    qt.set_size(wnd, 0.8, 0.8)
    wnd.show()
    sys.exit(app.exec())