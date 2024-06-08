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
from datetime import datetime

from msfx.lib.util.globals import is_valid_iso_date, is_valid_iso_time, is_valid_iso_datetime, is_valid_integer, \
    is_valid_float

def print_chk(label: str, value: str, check: bool):
    label = label.ljust(25)
    value = value.ljust(30)
    print(f"{label} {value} {check}")

print_chk("Valid ISO date", "2023-12-31", is_valid_iso_date("2023-12-31"))
print_chk("Valid ISO date", "2023-12-1a", is_valid_iso_date("2023-12-1a"))
print_chk("Valid ISO time", "12:25:00", is_valid_iso_time("12:25:00"))
print_chk("Valid ISO time", "12:25:00.3433", is_valid_iso_time("12:25:00.3433"))
print_chk("Valid ISO date-time", "2023-12-31 12:25:00", is_valid_iso_datetime("2023-12-31 12:25:00"))
print_chk("Valid ISO date-time", "2023-12-31 12:25:00.895", is_valid_iso_datetime("2023-12-31 12:25:00.895"))
print_chk("Valid integer", "10", is_valid_integer("10"))
print_chk("Valid integer", "10.0", is_valid_integer("10.0"))
print_chk("Valid float", "10", is_valid_float("10"))
print_chk("Valid float", "10.0", is_valid_float("10.0"))
print_chk("Valid decimal", "10", is_valid_float("10"))
print_chk("Valid decimal", "10.0", is_valid_float("10.0"))

print(str(datetime.now()))