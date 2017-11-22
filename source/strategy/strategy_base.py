# encoding: UTF-8
from __future__ import print_function
from abc import ABCMeta, abstractmethod

class StrategyBase(metaclass=ABCMeta):
    """
    Base strategy class
    """
    def __init__(self, symbols, events_engine):
        self._symbols = symbols
        self._events_engine = events_engine
        self.name = ''
        self.author = ''
        self.initialized = False

    def on_start(self):
        self.initialized = True

    def on_stop(self):
        self.initialized = False

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

    def on_order(self):
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
