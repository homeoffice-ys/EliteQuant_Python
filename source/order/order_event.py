# encoding: UTF-8
from __future__ import print_function

from .order_status import *
from .order_type import *
from ..event.event import *

class OrderEvent(Event):
    """
    Order event
    """
    def __init__(self):
        """
        Initialises order
        """
        self.event_type = EventType.ORDER
        self.internal_order_id = -1
        self.broker_order_id = -1
        self.full_symbol = ''
        self.order_type = OrderType.MARKET
        self.order_status = OrderStatus.NONE
        self.limit_price = 0.0
        self.stop_price = 0.0
        self.size = 0         # short < 0, long > 0
        self.fill_price = 0.0
        self.fill_size = 0