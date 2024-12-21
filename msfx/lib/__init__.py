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


def check_class_name(arg, clazz):
    if arg is None: return
    arg_class = arg.__module__ + '.' + arg.__class__.__name__
    chk_class = clazz.__module__ + '.' + clazz.__name__
    if arg_class != chk_class: raise TypeError("{} expected to be {}".format(arg_class, chk_class))