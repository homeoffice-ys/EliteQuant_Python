#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtGui
from ..order.order_event import OrderEvent
from ..order.order_status import *

class OrderWindow(QtWidgets.QTableWidget):
    '''
    Order Monitor
    '''
    order_status_signal = QtCore.pyqtSignal(type(OrderStatusEvent()))

    def __init__(self, outgoing_queue, lang_dict, parent=None):
        super(OrderWindow, self).__init__(parent)

        self.header = [lang_dict['OrderID'],
                       lang_dict['Symbol'],
                       lang_dict['Name'],
                       lang_dict['Security_Type'],
                       lang_dict['Direction'],
                       lang_dict['Order_Flag'],
                       lang_dict['Price'],
                       lang_dict['Quantity'],
                       lang_dict['Filled'],
                       lang_dict['Status'],
                       lang_dict['Order_Time'],
                       lang_dict['Cancel_Time'],
                       lang_dict['Exchange'],
                       lang_dict['Account'],
                       lang_dict['Source']]
        self._orderids = []

        self.init_table()

        self._outgoingqueue = outgoing_queue
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

        self.itemDoubleClicked.connect(self.cancel_order)

    def update_table(self, orderevent):
        '''
        If order id exist, update status
        else append one row
        '''
        if str(orderevent.broker_order_id) in self._orderids:
            row = self._orderids.index(orderevent.broker_order_id)
            self.item(row, 9).setText(OrderStatus(int(orderevent.order_status)).name)
        else:  # including empty
            self._orderids.append(str(orderevent.broker_order_id))
            self.insertRow(0)
            self.setItem(0, 0, QtWidgets.QTableWidgetItem(orderevent.broker_order_id))
            self.setItem(0, 1, QtWidgets.QTableWidgetItem(orderevent.full_symbol))
            self.setItem(0, 2, QtWidgets.QTableWidgetItem(0))
            self.setItem(0, 9, QtWidgets.QTableWidgetItem(OrderStatus(int(orderevent.order_status)).name))

    def cancel_order(self,mi):
        row = mi.row()
        order_id = self.item(row, 0).text()
        self._outgoingqueue.put('c|' + order_id)

