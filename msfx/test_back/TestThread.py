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

from threading import Thread, Lock

counter = 0
lock = Lock()

def increment(num: int):
    global counter
    for _ in range(num):
        lock.acquire()
        counter += 1
        lock.release()

thread1 = Thread(target=increment, args=(10000000,))
thread2 = Thread(target=increment, args=(5000000,))

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print(counter)
print(thread1.is_alive())
print(thread2.is_alive())
