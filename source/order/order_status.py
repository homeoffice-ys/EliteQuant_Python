#!/usr/bin/env python
# -*- coding: utf-8 -*-
from enum import Enum
from ..event.event import *

class OrderStatus(Enum):
    NEWBORN = 0
    PENDING_SUBMIT = 1
    PENDING_CANCEL = 2
    SUBMITTED = 3
    ACKNOWLEDGED = 4
    CANCELED = 5
    FILLED = 6
    PARTIALLY_FILLED = 8
    API_PENDING = 9
    API_CANCELLED = 10
    ERROR = 11
    NONE = 12


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