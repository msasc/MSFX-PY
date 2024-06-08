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

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtGui import QIcon

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dynamic Button Addition')
        self.setGeometry(100, 100, 300, 200)

        # Central widget and layout
        self.centralWidget = QWidget(self)
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)

    def addButton(self, **kwargs):
        # Create the button
        button = QPushButton(kwargs.get('text', 'Default Text'))
        button.setObjectName(kwargs.get('name'))

        # Set the icon if provided
        if 'icon' in kwargs:
            button.setIcon(QIcon(kwargs['icon']))

        # Connect the action if provided
        if 'action' in kwargs and callable(kwargs['action']):
            # If action arguments are provided, use a lambda to pass them
            if 'action_args' in kwargs:
                # noinspection PyUnresolvedReferences
                button.clicked.connect(lambda: kwargs['action'](*kwargs['action_args']))
            else:
                # noinspection PyUnresolvedReferences
                button.clicked.connect(kwargs['action'])

        # Add the button to the layout
        self.layout.addWidget(button)

# Example action function
def exampleAction(text="Hello"):
    print(f"Action triggered: {text}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()

    # Example of adding buttons
    window.addButton(name='btn1', text='Click Me', action=exampleAction, action_args=('Button Clicked!',))
    window.addButton(name='btn2', text='Button 2', icon='path/to/icon.png', action=exampleAction)

    window.show()
    sys.exit(app.exec())
