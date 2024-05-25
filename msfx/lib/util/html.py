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

from io import StringIO

class HTML:
    """
    Utility class to write HTML text.
    """
    def __init__(self):
        self.__head: StringIO = StringIO()
        self.__style: StringIO = StringIO()
        self.__body: StringIO = StringIO()

    def __add_header_style(self, type: str, code: str, style: str) -> None:
        if code is None:
            raise Exception("No tag or class name provided")
        if style is None:
            raise Exception("No style provided")

        self.__style.write("\n")

        if type == "class":
            self.__style.write(".")

        self.__style.write(code)
        self.__style.write(" {")
        self.__style.write(style)
        self.__style.write("}")

    def __print_style(self, style: str) -> None:
        self.__body.write(" style=")
        self.__body.write('"')
        styles = style.split(";")
        for style in styles:
            if not style.strip() == "":
                self.__body.write(" ")
                self.__body.write(style.strip())
                self.__body.write(";")
        self.__body.write('"')

    def add_header_tag_style(self, tag: str, style: str) -> None:
        """
        Add a tag style to the header.
        :param tag: The tag name
        :param style: The CSS style
        """
        self.__add_header_style("tag", tag, style)

    def add_header_class_style(self, clazz: str, style: str) -> None:
        """
        Add a tag style to the header.
        :param clazz: The class name
        :param style: The CSS style
        """
        self.__add_header_style("class", clazz, style)

    def tag_start(self, tag: str, clazz: str = None, style: str = None) -> None:

        if tag is None:
            raise Exception("Tag name is required")

        self.__body.write("\n")
        self.__body.write("<")
        self.__body.write(tag)

        if clazz is not None:
            self.__body.write(" class=")
            self.__body.write('"')
            self.__body.write(clazz)
            self.__body.write('"')

        if style is not None:
            self.__print_style(style)

        self.__body.write(">")

    def tag_end(self, tag: str):
        if tag is None:
            raise Exception("Tag name is required")
        self.__body.write("\n")
        self.__body.write("</")
        self.__body.write(tag)
        self.__body.write(">")

    def print(self, text: str, style: str = None) -> None:
        if text is None:
            raise Exception("Text is required")
        if style is not None:
            self.tag_start(tag="span", style=style)
        self.__body.write(text)
        if style is not None:
            self.tag_end(tag="span")

    def to_string(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        io: StringIO = StringIO()
        io.write("<!DOCTYPE html>")
        io.write("\n")
        io.write("<head>")
        io.write(self.__head.getvalue())
        io.write("\n")
        io.write("<style>")
        io.write(self.__style.getvalue())
        io.write("\n")
        io.write("</style>")
        io.write("\n")
        io.write("</head>")
        io.write("\n")
        io.write("<body>")
        io.write(self.__body.getvalue())
        io.write("\n")
        io.write("</body>")
        return io.getvalue()
