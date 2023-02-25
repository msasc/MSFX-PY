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

from msfx.db.meta import Value, OrderKey

k1 = OrderKey()
k1.append_segment(Value("A"))
k1.append_segment(Value("B"))
k1.append_segment(Value("C"))

k2 = OrderKey()
k2.append_segment(Value("C"))
k2.append_segment(Value("D"))

print(k1.compare_to(k2))
print(k1 < k2)
print(k1 == k2)

k3 = OrderKey()
k3.append_segment(Value("A"))
k3.append_segment(Value("B"))

k4 = OrderKey()
k4.append_segment(Value("A"))
k4.append_segment(Value("B"))

print(k3 == k4)
print(k3 > k4)

print(k1)

k5 = OrderKey()
k5.append_segment("A")
k5.append_segment("B")
k5.append_segment("C")
print(k5)