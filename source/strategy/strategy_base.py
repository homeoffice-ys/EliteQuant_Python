#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

class StrategyBase(metaclass=ABCMeta):
    """
    Base strategy class
    """
    def __init__(self, symbols, events_engine):
        """
        initialize trategy
        :param symbols:
        :param events_engine:backtest_event_engine or live_event engine that provides queue_.put()
        """
        self._symbols = symbols
        self._events_engine = events_engine
        self.id = -1
        self.capital = 0.0
        self.name = ''
        self.author = ''
        self.initialized = False
        self.active = False

    def set_capital(self, capital):
        self.capital = capital

    def on_init(self):
        self.initialized = True

        # set params
        if setting:
            d = self.__dict__
            for key in self.paramList:
                if key in setting:
                    d[key] = setting[key]

    def on_start(self):
        self.active = True

    def on_stop(self):
        self.active = False

    def on_tick(self, event):
        """
        Respond to tick
        """
        pass

    def on_bar(self, event):
        """
        Respond to bar
        """
        pass

    def on_order_status(self):
        """
        on order acknowledged
        :return:
        """
        #raise NotImplementedError("Should implement on_order()")
        pass

    def on_cancel(self):
        """
        on order canceled
        :return:
        """
        pass

    def on_fill(self):
        """
        on order filled
        :return:
        """
        pass

    def place_order(self, o):
        self._events_engine.put(o)

    def cancel_order(self, oid):
        pass

    def cancel_all(self):
        """
        cancel all standing orders from this strategy id
        :return:
        """
        pass

class Strategies(StrategyBase):
    """
    Strategies is a collection of strategy
    Usage e.g.: strategy = Strategies(strategyA, DisplayStrategy())
    """
    def __init__(self, *strategies):
        self._strategies_collection = strategies

    def on_tick(self, event):
        for strategy in self._strategies_collection:
            strategy.on_tick(event)
