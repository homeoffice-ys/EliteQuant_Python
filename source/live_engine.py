#!/usr/bin/env python
from __future__ import absolute_import, division, print_function
import sys
import os
import yaml
from PyQt5 import QtCore, QtWidgets, QtGui
#from source.live_engine import LiveEngine
#from source.gui.main_window import MainWindow
from source.gui.ui_main_window import MainWindow
import atexit
from signal import signal, SIGINT, SIG_DFL
from os import kill
from multiprocessing import Process
try:
	from server.EliteQuant import tradingengine_    # windows
except ImportError:
	from server.libelitequant import tradingengine_   # linux

# https://stackoverflow.com/questions/4938723/what-is-the-correct-way-to-make-my-pyqt-application-quit-when-killed-from-the-co
signal(SIGINT, SIG_DFL)

def main():
    config = None
    try:
        path = os.path.abspath(os.path.dirname(__file__))
        config_file = os.path.join(path, 'config.yaml')
        with open(os.path.expanduser(config_file), encoding='utf8') as fd:
            config = yaml.load(fd)
    except IOError:
        print("config.yaml is missing")

    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow(config)
    mainWindow.show()

    sys.exit(app.exec_())

def start_server():
    print('Running python server.')
    server = tradingengine_()
    server.run()

def stop_server():
    global server_process
    kill(server_process.pid, SIGINT)

server_process = None

if __name__ == "__main__":
    server_process = Process(target=start_server)
    server_process.start()
    atexit.register(stop_server)

    main()