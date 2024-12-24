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

def square(arg_x):
    print("s: " + str(arg_x) + ", " + str(arg_x * arg_x))

def cube(arg_x):
    print("c: " + str(arg_x) + ", " + str(arg_x * arg_x * arg_x))

def double(arg_x):
    print("d: " + str(arg_x) + ", " + str(arg_x + arg_x))

if __name__ == '__main__':
    with Pool(1) as p:
        for x in [0, 1, 2, 3, 4, 5]:
            p.map(square, (x,))
            p.map(cube, (x,))
            p.map(double, (x,))

        # Wait for all tasks to complete and retrieve results
        # output = [result.get() for result in results]
        # print(output)