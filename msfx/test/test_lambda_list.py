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
# Define your conditions as a list of lambdas
conditions = [
    (lambda value: isinstance(value, bool), "BOOL"),
    (lambda value: isinstance(value, str), "STRING"),
    (lambda value: isinstance(value, int), "INTEGER"),
    # Add more conditions as needed
]

# Function to evaluate the conditions
def check_conditions(value, vtype):
    for condition, expected_type in conditions:
        if condition(value) and vtype == expected_type:
            return True
    return False

# Example usage
value = 345
vtype = "INTEGER"

if check_conditions(value, vtype):
    print("Condition met!")
else:
    print("Condition not met!")
