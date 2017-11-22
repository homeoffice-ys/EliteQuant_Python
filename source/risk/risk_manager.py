# encoding: UTF-8
from __future__ import print_function
from .risk_manager_base import RiskManagerBase

class PassThroughRiskManager(RiskManagerBase):
    def order_in_compliance(self, original_order):
        """
        Pass through the order without constraints
        """
        return original_order
