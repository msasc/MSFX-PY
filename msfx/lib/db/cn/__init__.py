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

""" Defines an simple interface that SQL databases connectors must implement. """

from abc import ABC, abstractmethod

class DBCursor(ABC):
    @abstractmethod
    def execute(self, operation, **parameters): pass
    @abstractmethod
    def fetchone(self) -> object: pass
    @abstractmethod
    def fetchall(self) -> object: pass
    @abstractmethod
    def fetchmany(self, size=100) -> object: pass
    @abstractmethod
    def count(self) -> int: pass
    @abstractmethod
    def description(self) -> object: pass
    @abstractmethod
    def close(self): pass

class DBConnection(ABC):
    @abstractmethod
    def close(self): pass
    @abstractmethod
    def commit(self): pass
    @abstractmethod
    def rollback(self): pass
    @abstractmethod
    def cursor(self, **parameters) -> DBCursor: pass

class DBConnectionPool(ABC):
    @abstractmethod
    def get_connection(self) -> DBConnection: pass
    @abstractmethod
    def close(self): pass

