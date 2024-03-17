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
Contains PyQT6 utilities.
"""

from PyQt6 import QtCore, QtWidgets, QtGui

def set_size(widget: QtWidgets.QWidget, width_factor: float, height_factor: float):
    """
    Set the size of a widget relative to the primary screen size.
    :param widget: The widget to resize.
    :param width_factor: The width factor to apply to the widget.
    :param height_factor: The height factor to apply to the widget.
    :return: None
    """
    screen_size = QtGui.QGuiApplication.primaryScreen().size()
    width = screen_size.width() * width_factor
    height = screen_size.height() * height_factor
    widget.resize(int(width), int(height))
