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

from enum import Enum
from datetime import datetime

class TaskState(Enum):
    """ Enumeration of possible task states. """
    READY = "READY"
    """ Task is ready to start execution. """
    RUNNING = "RUNNING"
    """ Task is running. """
    SUCCEEDED = "SUCCEEDED"
    """ Task has finishes successfully. """
    CANCELLED = "CANCELLED"
    """ Task was cancelled. """
    FAILED = "FAILED"
    """ Task failed with an exception. """

class TaskProgress:
    def __init__(self):
        self.state = TaskState.READY

        self.start_time: datetime or None = None
        self.end_time: datetime or None = None

        self.message: str or None = None
        self.work_done: int or None = None
        self.total_work: int or None = None

        self.exception: Exception or None = None

        self.current_time: datetime or None = None
        self.elapsed_duration: datetime or None = None
        self.expected_duration: datetime or None = None
        self.expected_end_time: datetime or None = None

