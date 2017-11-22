# encoding: UTF-8
from __future__ import print_function

from enum import Enum

# OrderType.MKT.name == 'MKT'  OderType.MKT.value == 0
class OrderType(Enum):
    MARKET = 0
    LIMIT = 2
    STOP = 5
    STOP_LIMIT = 6
    TRAIING_STOP = 7