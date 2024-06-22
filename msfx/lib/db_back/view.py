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
from msfx.lib.db_back.column import ColumnList, Column
from msfx.lib.db_back.order import Order
from msfx.lib.db_back.relation import Relation
from msfx.lib.db_back.table import Table
from msfx.lib.util.globals import error_msg

class ColumnListView(ColumnList):
    def __init__(self, view):
        super(ColumnListView, self).__init__()
        self.__view = view

    def append(self, column: Column):
        column.set_view(self.__view)
        super().append(column)

class OrderBy(Order):
    def __init__(self, view):
        super(OrderBy, self).__init__()
        self.__view = view


class View:
    """ A view definition"""
    def __init__(self):
        self.__master_table = None
        self.__relations = []
        self.__columns = ColumnListView(self)
        self.__order_by = None

    def get_master_table(self):
        return self.__master_table
    def set_master_table(self, master_table: Table):
        self.__master_table = master_table

    def columns(self):
        return self.__columns

    def append_relation(self, relation):
        if relation is not None:
            if not isinstance(relation, Relation):
                error = error_msg("type error", "relation", relation, (Relation,))
                raise TypeError(error)
            self.__relations.append(relation)
    def clear_relations(self):
        self.__relations.clear()
    def get_relations(self):
        return list(self.__relations)
