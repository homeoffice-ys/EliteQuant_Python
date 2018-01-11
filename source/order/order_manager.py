#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .order_type import *
from datetime import datetime

class OrderManager(object):
    '''
    Manage/track all the orders
    '''
    def __init__(self):
        self._internal_order_id = 0         # unique internal_orderid
        self._order_dict = {}              # internal_order_id ==> order
        self._fill_dict = {}                # internal_fill_id ==> fill

    def reset(self):
        self._order_dict.clear()
        self._fill_dict.clear()

    def on_order(self, o):
        if o.internal_order_id < 0:         # internal_order_id not yet assigned
            o.internal_order_id = self._internal_order_id
            o.order_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self._internal_order_id = self._internal_order_id + 1
            self._order_dict[o.internal_order_id] = o

            # TODO: check order compliance and actually send out order

    def on_cancel(self, o):
        pass

    def on_fill(self, o):
        pass

    def retrieve_order(self, internal_order_id):
        try:
            return self._order_dict[internal_order_id]
        except:
            return None

    def retrieve_fill(self, internal_fill_id):
        try:
            return self._fill_dict[internal_fill_id]
        except:
            return None

