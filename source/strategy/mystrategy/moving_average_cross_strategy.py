#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import deque
import numpy as np

from ..strategy_base import StrategyBase
from ...order.order_event import OrderEvent
from ...order.order_type import OrderType


class MovingAverageCrossStrategy(StrategyBase):
    """
	classical MovingAverageCrossStrategy, golden cross
    """

    def __init__(
            self, events_engine, data_board,
            short_window=50, long_window=200
    ):
        super(MovingAverageCrossStrategy, self).__init__(events_engine, data_board)
        self.short_window = short_window
        self.long_window = long_window
        self.bars = 0
        self.invested = False
        self.prices = []

    def on_bar(self, bar_event):
        print('Processing {}'.format(bar_event.bar_start_time))
        symbol = bar_event.full_symbol
        hist_price = self._data_board.get_hist_price(symbol, bar_event.bar_start_time)

        # wait for enough bars
        if hist_price.shape[0] >= self.long_window:
            # Calculate the simple moving averages
            short_sma = np.mean(hist_price['Close'][-self.short_window:])
            long_sma = np.mean(hist_price['Close'][-self.long_window:])
            # Trading signals based on moving average cross
            if short_sma > long_sma and not self.invested:
                print("Long: %s, short_sma %s, long_sma %s" % ( bar_event.bar_end_time(), str(short_sma), str(long_sma) ))
                o = OrderEvent()
                o.full_symbol = symbol
                o.order_type = OrderType.MARKET
                o.order_size = 100
                self.place_order(o)
                self.invested = True
            elif short_sma < long_sma and self.invested:
                print("Short: %s, short_sma %s, long_sma %s" % (bar_event.bar_end_time(), str(short_sma), str(long_sma)))
                o = OrderEvent()
                o.full_symbol = symbol
                o.order_type = OrderType.MARKET
                o.order_size = -100
                self.place_order(o)
                self.invested = False
