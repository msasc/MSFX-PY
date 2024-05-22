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

from PyQt6.QtWidgets import (
    QApplication, QPushButton
)

from msfx.lib.qt.alert import QAlert

def action_button(**kwargs):
    name = kwargs.get("name")
    age = kwargs.get("age")
    gender = kwargs.get("gender")
    print(f"Name: {name}, age: {age}, gender: {gender}")


if __name__ == "__main__":
    app = QApplication([])
    alert = QAlert()
    alert.setSize(0.5, 0.5)

    butt = QPushButton("Button 1")
    butt.setObjectName("B1")
    alert.addButton(button=butt, accept=True)

    butt = QPushButton("Button 2")
    butt.setObjectName("B2")
    alert.addButton(button=butt, accept=True, action=action_button,
                    action_kwargs={'name': 'Michael', 'age': 50, 'gender': 'male'})

    alert.addButton(name="B3", text="Button 3", cancel=True)

    alert.setTypeWarning()
    result = alert.show()

    print(result)
    print(alert.wasAccepted())
