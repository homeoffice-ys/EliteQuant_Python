#!/usr/bin/env python
# -*- coding: utf-8 -*-
# http://stackoverflow.com/questions/9957195/updating-gui-elements-in-multithreaded-pyqt
import sys
import os
import webbrowser
import psutil
from queue import Queue, Empty
from PyQt5 import QtCore, QtWidgets, QtGui

from source.event.event import EventType
from source.order.order_status import OrderFlag
from .ui_market_window import MarketWindow
from .ui_order_window import OrderWindow
from .ui_fill_window import FillWindow
from .ui_position_window import PositionWindow
from .ui_account_window import AccountWindow
from .ui_strategy_window import StrategyWindow
from source.event.event import GeneralEvent
from source.strategy.mystrategy import strategy_list
from source.strategy.strategy_manager import StrategyManager
from source.event.live_event_engine import LiveEventEngine
from source.event.client_mq import ClientMq

class MainWindow(QtWidgets.QMainWindow):
    general_msg_signal = QtCore.pyqtSignal(GeneralEvent)
    def __init__(self, symbols, lang_dict):
        super(MainWindow, self).__init__()

        ## member variables
        self._symbols = symbols
        self._lang_dict = lang_dict
        self._font = lang_dict['font']
        self._widget_dict = {}
        self.central_widget = None
        self.market_window = None
        self.message_window = None
        self.order_window = None
        self.fill_window = None
        self.position_window = None
        self.account_window = None
        self.strategy_window = None
        self._outgoing_queue = Queue()

        # 1. set up gui windows
        self.setGeometry(50,50,600,400)
        self.setWindowTitle(lang_dict['Prog_Name'])
        self.setWindowIcon(QtGui.QIcon("gui/image/logo.ico"))
        self.init_menu()
        self.init_status_bar()
        self.init_central_area()

        ## 2. event engine
        self._events_engine = LiveEventEngine()

        ## 3. strategy_manager
        self._strategy_manager = StrategyManager(self._client_config, self._events_engine)
        ## 3. read strategies
        # self.strategies = strategy_list.keys()

        ## 4. client mq
        self._client_mq = ClientMq(self._events_engine, self._strategy_manager,self._outgoing_queue)

        ## 4. wire up event handlers
        self._events_engine.register_handler(EventType.TICK, self.market_window.tick_signal.emit)
        self._events_engine.register_handler(EventType.ORDERSTATUS, self.order_window.order_status_signal.emit)
        self._events_engine.register_handler(EventType.FILL, self.fill_window.fill_signal.emit)
        self._events_engine.register_handler(EventType.GENERAL, self.general_msg_signal.emit)
        self.general_msg_signal.connect(self.add_message)

        ## 5. start
        self._events_engine.start()
        self._client_mq.start()

    def set_font(self, font):
        self._font = font

    def init_menu(self):
        menubar = self.menuBar()

        sysMenu = menubar.addMenu(self._lang_dict['File'])
        # open folder
        sys_folderAction = QtWidgets.QAction(self._lang_dict['Folder'], self)
        sys_folderAction.setStatusTip(self._lang_dict['Open_Folder'])
        sys_folderAction.triggered.connect(self.open_proj_folder)
        sysMenu.addAction(sys_folderAction)

        sysMenu.addSeparator()

        # sys|exit
        sys_exitAction = QtWidgets.QAction(self._lang_dict['Exit'], self)
        sys_exitAction.setShortcut('Ctrl+Q')
        sys_exitAction.setStatusTip(self._lang_dict['Exit_App'])
        sys_exitAction.triggered.connect(self.close)
        sysMenu.addAction(sys_exitAction)

    def init_status_bar(self):
        self.statusthread = StatusThread()
        self.statusthread.status_update.connect(self.update_status_bar)
        self.statusthread.start()

    def init_central_area(self):
        self.central_widget = QtWidgets.QWidget()

        hbox = QtWidgets.QHBoxLayout()

        #-------------------------------- Top Left ------------------------------------------#
        topleft = MarketWindow(self._symbols, self._lang_dict)
        self.market_window = topleft

        # -------------------------------- Top right ------------------------------------------#
        topright = QtWidgets.QFrame()
        topright.setFrameShape(QtWidgets.QFrame.StyledPanel)
        topright.setFont(self._font)
        place_order_layout = QtWidgets.QFormLayout()
        self.sym = QtWidgets.QLineEdit()
        self.sym_name = QtWidgets.QLineEdit()
        self.sec_type = QtWidgets.QComboBox()
        self.sec_type.addItems([self._lang_dict['Stock'], self._lang_dict['Future'], self._lang_dict['Option'], self._lang_dict['Forex']])
        self.direction = QtWidgets.QComboBox()
        self.direction.addItems([self._lang_dict['Long'], self._lang_dict['Short']])
        self.order_flag = QtWidgets.QComboBox()
        self.order_flag.addItems([self._lang_dict['Open'], self._lang_dict['Close'], self._lang_dict['Close_Yesterday'], self._lang_dict['Close_Today']])
        self.order_price = QtWidgets.QLineEdit()
        self.order_quantity = QtWidgets.QLineEdit()
        self.order_type = QtWidgets.QComboBox()
        self.order_type.addItems([self._lang_dict['MKT'], self._lang_dict['LMT'], self._lang_dict['FAK'], self._lang_dict['FOK']])
        self.exchange = QtWidgets.QComboBox()
        self.exchange.addItems(['CFFEX','SHFE', 'DCE', 'HKFE','GLOBEX','SMART'])
        self.account = QtWidgets.QComboBox()
        self.account.addItems(['FROM', 'CONFIG'])
        self.btn_order = QtWidgets.QPushButton(self._lang_dict['Place_Order'])
        self.btn_order.clicked.connect(self.place_order)

        place_order_layout.addRow(QtWidgets.QLabel(self._lang_dict['Discretionary']))
        place_order_layout.addRow(self._lang_dict['Symbol'], self.sym)
        place_order_layout.addRow(self._lang_dict['Name'], self.sym_name)
        place_order_layout.addRow(self._lang_dict['Security_Type'], self.sec_type)
        place_order_layout.addRow(self._lang_dict['Direction'], self.direction)
        place_order_layout.addRow(self._lang_dict['Order_Flag'], self.order_flag)
        place_order_layout.addRow(self._lang_dict['Price'], self.order_price)
        place_order_layout.addRow(self._lang_dict['Quantity'], self.order_quantity)
        place_order_layout.addRow(self._lang_dict['Order_Type'], self.order_type)
        place_order_layout.addRow(self._lang_dict['Exchange'], self.exchange)
        place_order_layout.addRow(self._lang_dict['Account'], self.account)
        place_order_layout.addRow(self.btn_order)
        topright.setLayout(place_order_layout)

        # -------------------------------- bottom Left ------------------------------------------#
        bottomleft = QtWidgets.QTabWidget()
        bottomleft.setFont(self._font)
        tab1 = QtWidgets.QWidget()
        tab2 = QtWidgets.QWidget()
        tab3 = QtWidgets.QWidget()
        tab4 = QtWidgets.QWidget()
        tab5 = QtWidgets.QWidget()
        bottomleft.addTab(tab1, self._lang_dict['Log'])
        bottomleft.addTab(tab2, self._lang_dict['Order'])
        bottomleft.addTab(tab3, self._lang_dict['Fill'])
        bottomleft.addTab(tab4, self._lang_dict['Position'])
        bottomleft.addTab(tab5, self._lang_dict['Account'])

        # TODO: use table, add timestamp
        self.message_window = QtWidgets.QTextEdit()
        self.message_window.setReadOnly(True)
        self.message_window.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.message_window.moveCursor(QtGui.QTextCursor.End)
        msg_scroll_bar = self.message_window.verticalScrollBar()
        msg_scroll_bar.setValue(msg_scroll_bar.maximum())
        tab1_layout = QtWidgets.QVBoxLayout()
        tab1_layout.addWidget(self.message_window)
        tab1.setLayout(tab1_layout)

        self.order_window = OrderWindow(self._outgoing_queue, self._lang_dict)       # cancel_order outgoing nessage
        tab2_layout = QtWidgets.QVBoxLayout()
        tab2_layout.addWidget(self.order_window)
        tab2.setLayout(tab2_layout)

        self.fill_window =FillWindow(self._lang_dict)
        tab3_layout = QtWidgets.QVBoxLayout()
        tab3_layout.addWidget(self.fill_window)
        tab3.setLayout(tab3_layout)

        self.position_window = PositionWindow(self._lang_dict)
        tab4_layout = QtWidgets.QVBoxLayout()
        tab4_layout.addWidget(self.position_window)
        tab4.setLayout(tab4_layout)

        self.account_window = AccountWindow(self._lang_dict)
        tab5_layout = QtWidgets.QVBoxLayout()
        tab5_layout.addWidget(self.account_window)
        tab5.setLayout(tab5_layout)

        # -------------------------------- bottom right ------------------------------------------#
        bottomright = QtWidgets.QFrame()
        bottomright.setFrameShape(QtWidgets.QFrame.StyledPanel)
        bottomright.setFont(self._font)
        strategy_manager_layout = QtWidgets.QFormLayout()
        self.strategy_window = StrategyWindow(self._lang_dict)
        self.btn_strat_start = QtWidgets.QPushButton(self._lang_dict['Start_Strat'])
        self.btn_strat_pause = QtWidgets.QPushButton(self._lang_dict['Pause_Strat'])
        self.btn_strat_stop = QtWidgets.QPushButton(self._lang_dict['Stop_Strat'])
        self.btn_strat_liquidate = QtWidgets.QPushButton(self._lang_dict['Liquidate_Strat'])
        btn_strat_layout = QtWidgets.QHBoxLayout()
        btn_strat_layout.addWidget(self.btn_strat_start)
        btn_strat_layout.addWidget(self.btn_strat_pause)
        btn_strat_layout.addWidget(self.btn_strat_stop)
        btn_strat_layout.addWidget(self.btn_strat_liquidate)

        strategy_manager_layout.addRow(QtWidgets.QLabel(self._lang_dict['Automatic']))
        strategy_manager_layout.addRow(self.strategy_window)
        strategy_manager_layout.addRow(btn_strat_layout)
        bottomright.setLayout(strategy_manager_layout)

        # --------------------------------------------------------------------------------------#
        splitter1 = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter1.addWidget(topleft)
        splitter1.addWidget(topright)
        splitter1.setSizes([400,100])

        splitter2 = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter2.addWidget(bottomleft)
        splitter2.addWidget(bottomright)
        splitter2.setSizes([400, 100])

        splitter3 = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        splitter3.addWidget(splitter1)
        splitter3.addWidget(splitter2)
        splitter3.setSizes([400, 100])

        hbox.addWidget(splitter3)
        self.central_widget.setLayout(hbox)
        self.setCentralWidget(self.central_widget)

    def update_status_bar(self, message):
        self.statusBar().showMessage(message)

    def add_message(self, general_event):
        self.message_window.append(general_event.content)

    def open_proj_folder(self):
        webbrowser.open('d:/workspace/elitequant_python/')

    def place_order(self):
        s = str(self.sym.text())
        n = self.direction.currentIndex()
        f = str(self.order_flag.currentIndex())
        p = str(self.order_price.text())
        q = str(self.order_quantity.text())
        t = self.order_type.currentIndex()

        if (t == 0):
            msg = 'o|MKT|' + s + '|' + (q if (n==0) else '-'+q)
            print('send msg: ' + msg)
            self._outgoing_queue.put(msg)
        elif (t == 1):
            msg = 'o|LMT|' + s + '|' + (q if (n==0) else '-'+q) +  '|' + p + '|' +  f
            print('send msg: ' + msg)
            self._outgoing_queue.put(msg)
        else:
            pass

    def closeEvent(self, a0: QtGui.QCloseEvent):
        print('closing main window')
        self._events_engine.stop()
        self._client_mq.stop()

class StatusThread(QtCore.QThread):
    status_update = QtCore.pyqtSignal(str)

    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        while True:
            cpuPercent = psutil.cpu_percent()
            memoryPercent = psutil.virtual_memory().percent
            self.status_update.emit('CPU Usage: ' + str(cpuPercent) + '% Memory Usage: ' + str(memoryPercent) + '%')
            self.sleep(1)