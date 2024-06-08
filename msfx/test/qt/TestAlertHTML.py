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
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtWidgets import (
    QApplication, QPushButton, QSizePolicy
)

from msfx.lib.qt.alert import QAlert
from msfx.lib.qt.canvas import QCanvas
from msfx.lib.util.html import HTML

def action_button(**kwargs):
    name = kwargs.get("name")
    age = kwargs.get("age")
    gender = kwargs.get("gender")
    print(f"Name: {name}, age: {age}, gender: {gender}")

def paintCanvas():
    width = canvas.width()
    height = canvas.height()

    factor = 0.98

    x = int(width * (1 - factor) / 2)
    y = int(height * (1 - factor) / 2)
    w = int(width * factor)
    h = int(height * factor)

    # w = min(w, h)
    # h = min(w, h)

    painter: QPainter = canvas.startPaint()
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(QPen(QColor('black'), 1))
    painter.drawEllipse(x, y, w, h)
    canvas.endPaint()


if __name__ == "__main__":
    app = QApplication([])
    alert = QAlert()
    alert.setSize(0.5, 0.5)

    button_style = \
        "font-size: 14pt; "\
        "font-family: 'Times New Roman';"\
        "padding-top: 5px; "\
        "padding-left: 10px;"\
        "padding-right: 10px;"\
        "padding-bottom: 5px;"

    butt = QPushButton("Button 1")
    butt.setObjectName("B1")
    alert.addButton(button=butt,
                    accept=True,
                    style=button_style)

    butt = QPushButton("Button 2")
    butt.setObjectName("B2")
    alert.addButton(button=butt,
                    action=action_button,
                    action_kwargs={'name': 'Michael', 'age': 50, 'gender': 'male'},
                    style=button_style)

    alert.addButton(name="B3",
                    text="Button 3",
                    cancel=True,
                    style=button_style)

    html = HTML()
    html.print("Hello my friend, is it me you're looking for?",
               style="font-size: 14pt; font-family: 'Times New Roman'")
    html.tag_start(tag="p")
    html.print("Oh no!",
               style="font-size: 24pt; font-family: 'Times New Roman'; color: red;")

    html_str = html.to_string()
    print(html_str)

    # alert.setText(html_str)

    canvas = QCanvas()
    canvas.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
    canvas.paintCanvas.connect(paintCanvas)
    alert.setCentralWidget(canvas)

    alert.setTitle("This is a title",
                   "font-weight: plain;"
                   "font-size: 18pt;"
                   "font-family: 'Times New Roman', 'Serif';"
                   "padding-bottom: 10px;"
                   "qproperty-alignment: 'AlignCenter';")

    alert.setTypeQuestion()
    result = alert.show()

    print(result)
    print(alert.wasAccepted())

    # sys.exit(app.exec())
