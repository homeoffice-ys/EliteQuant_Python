#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtGui
from ..order.fill_event import FillEvent

class AccountWindow(QtWidgets.QTableWidget):
    fill_signal = QtCore.pyqtSignal(type(FillEvent()))

    def __init__(self, lang_dict, parent=None):
        super(AccountWindow, self).__init__(parent)

        self.header = [lang_dict['AccountID'],
                       lang_dict['Yesterday_Net'],
                       lang_dict['Net'],
                       lang_dict['Available'],
                       lang_dict['Commission'],
                       lang_dict['Margin'],
                       lang_dict['Closed_PnL'],
                       lang_dict['Open_PnL'],
                       lang_dict['Brokerage'],
                       lang_dict['API']]

        self.init_table()
        self._lang_dict = lang_dict
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
        self.setItem(0, 2, QtWidgets.QTableWidgetItem(fillevent.full_symbol))
        self.setItem(0, 7, QtWidgets.QTableWidgetItem(fillevent.fill_price))
        self.setItem(0, 8, QtWidgets.QTableWidgetItem(fillevent.fill_size))
        self.setItem(0, 9, QtWidgets.QTableWidgetItem(fillevent.timestamp))

