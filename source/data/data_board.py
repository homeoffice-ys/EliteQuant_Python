#!/usr/bin/env python
# -*- coding: utf-8 -*-
class DataBoard(object):
    """
    Data tracker that holds current market data info
    """
    def __init__(self):
        self._symbols = {}

    def on_tick(self, tick):
        if tick.full_symbol not in self._symbols:
            self._symbols[tick.full_symbol]  = {}

        self._symbols[tick.full_symbol]['timestamp'] = tick.timestamp
        self._symbols[tick.full_symbol]['last_price'] = tick.price

    def on_bar(self, bar):
        if bar.full_symbol not in self._symbols:
            self._symbols[bar.full_symbol]  = {}

        self._symbols[bar.full_symbol]['timestamp'] = bar.bar_end_time()
        self._symbols[bar.full_symbol]['last_price'] = bar.close_price
        self._symbols[bar.full_symbol]['last_adj_price'] = bar.adj_close_price

    def get_last_price(self, symbol):
        """
        Returns the most recent actual timestamp for a given ticker
        """
        if symbol in self._symbols:
            return self._symbols[symbol]["last_adj_price"]
        else:
            print(
                "LastPrice for ticker %s is not found" % (symbol)
            )
            return None

    def get_last_timestamp(self, symbol):
        """
        Returns the most recent actual timestamp for a given ticker
        """
        if symbol in self._symbols:
            return self._symbols[symbol]["timestamp"]
        else:
            print(
                "Timestamp for ticker %s is not found" % (symbol)
            )
            return None