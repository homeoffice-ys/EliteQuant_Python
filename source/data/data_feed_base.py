# encoding: UTF-8
from __future__ import print_function
from abc import ABCMeta, abstractmethod

class DataFeedBase(metaclass=ABCMeta):
    """
    DateFeed baae class
    """

    @abstractmethod
    def subscribe_market_data(self, symbols):
        """subscribe to market data"""

    @abstractmethod
    def unsubscribe_market_data(self, symbols):
        """unsubscribe market data"""

    @abstractmethod
    def stream_next(self):
        """stream next data event"""