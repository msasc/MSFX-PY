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

# html = '<h1>Hello, World!</h1><p>This is <b>rich text</b> format content.'
# html += '<p>'
# html += '<table style="border: none; border-collapse: collapse;">'
# html += '<tr>'
# html += '<td style="border: 1px solid rgb(180,180,180);">Column 1</td>'
# html += '<td style="border: 1px solid rgb(180,180,180);">Column 2</td>'
# html += '</tr>'
# html += '</table>'

html = ''
# html += '<!DOCTYPE html>'
# html += '<html>'
# html += '<head>'
# html += '<style>'
# html += 'body {background-color: powderblue;}'
# html += 'h1 {color: blue;}'
# html += 'p {color: red;}'
# html += '</style>'
# html += '</head>'
# html += '<body>'
#
# html += '<h1>This is a heading</h1>'
# html += '<p>This is a paragraph.</p>'
#
# html += '</body>'
# html += '</html>'

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
html += '</body>'
html += '</html>'


textBrowser.setHtml(html)
# textBrowser.setPlainText(html)
textBrowser.show()
app.exec()
