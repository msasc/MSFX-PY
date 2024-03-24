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

from PyQt6.QtWidgets import QApplication, QTextBrowser

app = QApplication([])
textBrowser = QTextBrowser()

html = '<h1>Hello, World!</h1><p>This is <b>rich text</b> format content.'
html += '<p>'
html += '<table style="border: none; border-collapse: collapse;">'
html += '<tr>'
html += '<td style="border: 1px solid rgb(180,180,180);">Column 1</td>'
html += '<td style="border: 1px solid rgb(180,180,180);">Column 2</td>'
html += '</tr>'
html += '</table>'

textBrowser.setHtml(html)
textBrowser.show()
app.exec()
