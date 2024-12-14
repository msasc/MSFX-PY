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

from msfx.lib_back.qt.alert import QAlert

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
    alert.addButton(button=butt, action=action_button,
                    action_kwargs={'name': 'Michael', 'age': 50, 'gender': 'male'})

    alert.addButton(name="B3", text="Button 3", cancel=True)

    html = ''
    html += '<!DOCTYPE html>'
    html += '<html>'
    html += '<head>'
    html += '    <title>Class Style Example</title>'
    html += '    <style>'
    html += '        .box {'
    html += '            width: 100px;'
    html += '            height: 100px;'
    html += '            background-color: lightgray;'
    html += '            margin: 10px;'
    html += '            display: inline-block;'
    html += '            line-height: 100px;'
    html += '            text-align: center;'
    html += '        }'

    html += '        .highlighted {'
    html += '            background-color: yellow;'
    html += '        }'

    # color = getBackgroundColor(QLabel())
    #
    # html += '        body {'
    # html += '            background-color: ' + toRGB(color) + ';'
    # html += '        }'

    html += '        .text {'
    html += '            font-family: Arial, sans-serif;'
    html += '            color: #333;'
    html += '        }'

    html += '        .text.highlighted {'
    html += '            color: red;'
    html += '            font-weight: bold;'
    html += '        }'
    html += '    </style>'
    html += '</head>'
    html += '<body>'
    html += '    <div class="box">Box 1</div>'
    html += '    <div class="box highlighted">Box 2 (Highlighted)</div>'
    html += '    <p class="text">This is some text.</p>'
    html += '    <p class="text highlighted">This is some highlighted text.</p>'
    html += '    <p class="text">This is some text.</p>'
    html += '    <p class="text">This is some text.</p>'
    html += '    <p class="text">This is some text.</p>'
    html += '    <p class="text">This is some text.</p>'
    html += '    <p class="text">This is some text.</p>'
    html += '    <p class="text">This is some text.</p>'
    html += '    <p class="text">This is some text.</p>'
    html += '    <p class="text">This is some text.</p>'
    html += '    <p class="text">This is some text.</p>'
    html += '    <p class="text">This is some text.</p>'
    html += '    <p class="text">This is some text.</p>'
    html += '    <p class="text">This is some text.</p>'
    html += '    <p class="text">This is some text.</p>'
    html += '</body>'
    html += '</html>'

    alert.setText(html)

    alert.setTitle("This is a title",
                   " font-weight: bold; "
                   " font-size: 24px;"
                   "font-family: 'Times New Roman', 'Serif';"
                   "padding-bottom: 10px;"
                   "qproperty-alignment: 'AlignCenter';")

    alert.setTypeWarning()
    result = alert.show()

    print(result)
    print(alert.wasAccepted())

    # sys.exit(app.exec())
