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
Contains PyQT6 utility functions.

It is a formatting convention in Python that function or member names are in
lower case with words separated by an underscore. But in this qt module we
will follow the C++ convention that is used by all names in PyQt.
"""
from PyQt6.QtGui import QGuiApplication, QColor
from PyQt6.QtWidgets import QWidget

def setWidgetSize(widget: QWidget, widthFactor: float, heightFactor: float):
    """
    Set the size of a widget relative to the primary screen size.
    :param widget: The widget to resize.
    :param widthFactor: The width factor to apply to the widget.
    :param heightFactor: The height factor to apply to the widget.
    :return: None
    """
    screenSize = QGuiApplication.primaryScreen().size()
    width = screenSize.width() * widthFactor
    height = screenSize.height() * heightFactor
    widget.resize(int(width), int(height))

def getBackgroundColor(widget):
    palette = widget.palette()
    color = palette.color(widget.backgroundRole())
    return color

def setBackgroundColor(widget: QWidget, color: QColor):
    # Convert QColor to hex string
    color_name = color.name()
    # Set the stylesheet to change the background color
    widget.setStyleSheet(f"background-color: {color_name};")

def toRGB(color):
    red = color.red()
    green = color.green()
    blue = color.blue()
    return f"rgb({red}, {green}, {blue})"