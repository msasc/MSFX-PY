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

from msfx.db.meta import Types, Field, Order

f_CARTICLE = Field()
f_CARTICLE.set_name("CARTICLE")
f_CARTICLE.set_type(Types.STRING)
f_CARTICLE.set_length(40)

f_CCOMPONENT = Field(f_CARTICLE)
f_CCOMPONENT.set_name("CCOMPONENT")

order: Order = Order()
order.add_segment(f_CARTICLE)
order.add_segment(f_CCOMPONENT, False)

print(order)

for segment in order:
    print(segment.get_field())

