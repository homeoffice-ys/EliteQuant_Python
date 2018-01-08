#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtGui
from ..order.order_event import OrderEvent
from ..order.order_status import *

class StrategyWindow(QtWidgets.QTableWidget):
    '''
    Order Monitor
    '''
    order_status_signal = QtCore.pyqtSignal(type(OrderStatusEvent()))

    def __init__(self, lang_dict, parent=None):
        super(StrategyWindow, self).__init__(parent)

        self.header = [lang_dict['SID'],
                       lang_dict['SName'],
                       lang_dict['nHoldings'],
                       lang_dict['nTrades'],
                       lang_dict['Open_PnL'],
                       lang_dict['Closed_PnL'],
                       lang_dict['Status']]

        self.init_table()

        self._lang_dict = lang_dict
        self.order_status_signal.connect(self.update_table)

    def init_table(self):
        col = len(self.header)
        self.setColumnCount(col)

        self.setHorizontalHeaderLabels(self.header)
        self.setEditTriggers(self.NoEditTriggers)
        self.verticalHeader().setVisible(False)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(False)

    def update_table(self, orderevent):
        pass