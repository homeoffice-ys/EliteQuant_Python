#!/usr/bin/env python
from __future__ import absolute_import, division, print_function

from PyQt5 import QtCore, QtWidgets, QtGui
from ..order.fill_event import FillEvent

class FillWindow(QtWidgets.QTableWidget):
    fill_signal = QtCore.pyqtSignal(type(FillEvent()))

    def __init__(self, parent=None):
        super(FillWindow, self).__init__(parent)

        self.header = ['OrderID', 'Symbol', 'FillTime', 'FillPrice', 'FillSize']

        self.init_table()
        self.fill_signal.connect(self.update_table)

    def init_table(self):
        col = len(self.header)
        self.setColumnCount(col)

        self.setHorizontalHeaderLabels(self.header)
        self.setEditTriggers(self.NoEditTriggers)
        self.verticalHeader().setVisible(False)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(False)

    def update_table(self,fillevent):
        '''
        Only add row
        '''
        self.insertRow(0)
        self.setItem(0, 0, QtWidgets.QTableWidgetItem(fillevent.broker_order_id))
        self.setItem(0, 1, QtWidgets.QTableWidgetItem(fillevent.full_symbol))
        self.setItem(0, 2, QtWidgets.QTableWidgetItem(fillevent.timestamp))
        self.setItem(0, 3, QtWidgets.QTableWidgetItem(fillevent.fill_price))
        self.setItem(0, 4, QtWidgets.QTableWidgetItem(fillevent.fill_size))

