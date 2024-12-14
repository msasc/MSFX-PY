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
from multiprocessing import Pool
import time

def my_task(x):
    print(f"Processing {x}")
    time.sleep(1)  # Simulate work by sleeping for 1 second
    return x * x

if __name__ == '__main__':
    with Pool(2) as p:  # Create a pool with 2 worker processes
        result = p.map(my_task, range(10))
    print(result)
