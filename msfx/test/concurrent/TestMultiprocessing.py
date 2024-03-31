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

from multiprocessing import Value, Process

def increment(counter):
    for _ in range(10000):
        with counter.get_lock():
            counter.value += 1

if __name__ == '__main__':
    counter = Value('i', 0)  # 'i' indicates a signed int
    processes = [Process(target=increment, args=(counter,)) for _ in range(10)]

    for p in processes:
        p.start()
    for p in processes:
        p.join()

    print(f"Counter value: {counter.value}")
