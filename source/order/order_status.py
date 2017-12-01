# encoding: UTF-8
from __future__ import print_function

from enum import Enum
from ..event.event import *

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


class OrderFlag(Enum):
    OPEN = 0
    CLOSE = 1
    CLOSE_TODAY = 2
    CLOSE_YESTERDAY = 3


class OrderStatusEvent(Event):
    """
    Order event
    """
    def __init__(self):
        """
        Initialises order
        """
        self.event_type = EventType.ORDERSTATUS
        self.internal_order_id = -1
        self.broker_order_id = -1
        self.full_symbol = ''
        self.order_status = OrderStatus.NONE