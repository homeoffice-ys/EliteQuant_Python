#!/usr/bin/env python
from __future__ import absolute_import, division, print_function

from PyQt5 import QtCore, QtWidgets, QtGui
from ..data.tick_event import TickEvent

class MarketWindow(QtWidgets.QTableWidget):
    tick_signal = QtCore.pyqtSignal(type(TickEvent()))

    def __init__(self, symbols, parent=None):
        super(MarketWindow, self).__init__(parent)

        self._symbols = symbols
        self.header = ['Symbol', 'Open', 'High', 'Low', 'Bid Size', 'Bid', 'Ask', 'Ask Size', 'Last', 'Last Size']

        self.init_table()
        self.tick_signal.connect(self.update_table)

    def init_table(self):
        row = len(self._symbols)
        self.setRowCount(row)
        col = len(self.header)
        self.setColumnCount(col)

        self.setHorizontalHeaderLabels(self.header)
        self.setEditTriggers(self.NoEditTriggers)
        self.verticalHeader().setVisible(False)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(False)

        for i in range(row):
            self.setItem(i, 0, QtWidgets.QTableWidgetItem(self._symbols[i]))
            for j in range(1,col):
                self.setItem(i, j, QtWidgets.QTableWidgetItem(0.0))

    def update_table(self,tickevent):
        if tickevent.full_symbol in self._symbols:
            row = self._symbols.index(tickevent.full_symbol)
            if (float(tickevent.price) > 0.0):
                self.item(row, 8).setText(str(tickevent.price))

