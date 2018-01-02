#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtGui
from ..data.tick_event import TickEvent

class MarketWindow(QtWidgets.QTableWidget):
    tick_signal = QtCore.pyqtSignal(type(TickEvent()))

    def __init__(self, symbols, lang_dict, parent=None):
        super(MarketWindow, self).__init__(parent)

        self._symbols = symbols
        self._lang_dict = lang_dict
        self.header = [lang_dict['Symbol'],
                       lang_dict['Name'],
                       lang_dict['Last_Price'],
                       lang_dict['Volume'],
                       lang_dict['Open_Interest'],
                       lang_dict['Bid_Size'],
                       lang_dict['Bid'],
                       lang_dict['Ask'],
                       lang_dict['Ask_Size'],
                       lang_dict['Yesterday_Close'],
                       lang_dict['Open_Price'],
                       lang_dict['High_Price'],
                       lang_dict['Low_Price'],
                       lang_dict['Time'],
                       lang_dict['Source']]

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
                self.item(row, 2).setText(str(tickevent.price))

