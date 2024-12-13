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

from abc import ABC, abstractmethod
from datetime import datetime
import os

class MkData(ABC):
    """
    MkData abstract class defines the interface for classes that provide market data,
    mainly for plotting charts.
    """
    @abstractmethod
    def get_ticker_info(self, **kwargs) -> tuple[str, str, str, str, int]:
        """
        Returns the ticker symbol information as a tuple with the following fields:

        The first field, a string, is an indicator of the market:
        - FX means Forex
        - ID means Index
        - ST means Stock

        The second field, a string, depends on the nature of the market:
        - If the market is Forex (FX) the second token is the primary currency code, for instance EUR.
        - If the market is an Index or a Stock, the second token is the identifier of the product,
          for example DAX, NDX, DJI, SAN.

        The third field, a string, also depends on the nature of the market:
        - If the market is Forex (FX) the third token is the secondary currency code, for example USD,
          and the final identifier for the product would be EUR/USD.

        The fourth field, a string is the time frame unit, either DAY or MIN, by day or minute.

        The fifth and final field is the number of units, 1, 7, 30, 240, etc.

        :param kwargs: Necessary parameters to retrieve the data.
        :return: The ticker data as a tuple with the explained fields.
        """
        pass
    @abstractmethod
    def get_ticker_data(self, **kwargs) -> list[tuple[datetime, float, float, float, float, float]]:
        """
        Return a list of tuples that conform the data from the source that offers market data.
        :param kwargs: Necessary parameters to retrieve the data.
        :return: A list of tuples: time, open, high, low, close, volume
        """
        pass

class MkDataVChart(MkData):
    """
    Implements MkData for Visual Chart exported txt files. By convention, VChart files have the
    name formatted with five tokens separated by an underscore, that represent the five items of
    the ticker info tuple.
    """
    def __init__(self):
        super().__init__()

    def get_ticker_info(self, **kwargs) -> tuple[str, str, str, str, int]:
        """
        Returns the ticker info.
        :param kwargs: Only one parameter, the key is "file_name" and the value is the file name.
        :return: The ticker info.
        """
        file_name = kwargs['file_name']
        file_name = os.path.basename(file_name)
        file_name = os.path.splitext(file_name)[0]
        keys = file_name.split("_")
        return keys[0], keys[1], keys[2], keys[3], int(keys[4])

    def get_ticker_data(self, **kwargs) -> list[tuple[datetime, float, float, float]]:
        pass