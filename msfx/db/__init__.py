#  Copyright (c) 2023 Miquel Sas.
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
msfx.db package enables Python programs to access SQL databases using an
interface detached from the underlying engine, be MariaDB, Postgresql,
Oracle or whatever has implemented an adapter.
"""

from msfx.db.meta import Types, Field

def create_field(name: str, type: Types, length: int or None = None, decimals: int or None = None) -> Field:
    """
    Create a basic field definition.
    :param name: The name.
    :param type: The type.
    :param length: Optional length.
    :param decimals: Optional decimals.
    :return: The field definition.
    """
    field: Field = Field()
    field.set_name(name)
    field.set_type(type)
    if length is not None:
        field.set_length(length)
    if decimals is not None:
        field.set_decimals(decimals)
    return field
