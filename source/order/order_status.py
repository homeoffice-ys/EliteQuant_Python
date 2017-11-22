# encoding: UTF-8
from __future__ import print_function

from enum import Enum

class OrderStatus(Enum):
    NONE = -1
    NEWBORN = 0
    PENDING_SUBMIT = 1
    PENDING_CANCEL = 2
    SUBMITTED = 3
    ACKNOWLEDGED = 4
    CANCELED = 5
    FILLED = 6
    PARTIALLY_FILLED = 8
