# encoding: UTF-8
from __future__ import print_function

from .order_type import *

class OrderManager(object):
    '''
    Manage/track all the orders
    '''
    def __init__(self):
        self._internal_order_id = 0         # unique internal_orderid
        self._order_dict = {}              # internal_order to [# sent, # filled, is_canceled,

    def place_order(self, o):
        if o.internal_order_id < 0:         # internal_order_id not yet assigned
            o.internal_order_id = self._internal_order_id
            self._internal_order_id = self._internal_order_id + 1
            self._order_dict[o.internal_order_id] = o

