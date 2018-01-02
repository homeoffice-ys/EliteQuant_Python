#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtGui
from ..order.fill_event import FillEvent

class PositionWindow(QtWidgets.QTableWidget):
    fill_signal = QtCore.pyqtSignal(type(FillEvent()))

    def __init__(self, lang_dict, parent=None):
        super(PositionWindow, self).__init__(parent)

        self.header = [lang_dict['Symbol'],
                       lang_dict['Name'],
                       lang_dict['Security_Type'],
                       lang_dict['Direction'],
                       lang_dict['Quantity'],
                       lang_dict['Yesterday_Quantity'],
                       lang_dict['Freezed'],
                       lang_dict['Average_Price'],
                       lang_dict['Open_PnL'],
                       lang_dict['Account'],
                       lang_dict['Source']]

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

