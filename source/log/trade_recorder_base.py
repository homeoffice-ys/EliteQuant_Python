# encoding: UTF-8
from __future__ import print_function

from abc import ABCMeta, abstractmethod

class AbstractTradeRecorder(object):
    """
    transaction recorder
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def record_trade(self, fill):
        """
        logs fill event
        """
        raise NotImplementedError("Should implement record_trade()")
