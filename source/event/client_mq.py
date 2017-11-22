# encoding: UTF-8
from __future__ import print_function

from threading import Thread
from nanomsg import Socket, PAIR, SUB, SUB_SUBSCRIBE, AF_SP
from source.data.tick_event import TickEvent
from source.event.event import GeneralEvent

class ClientMq(object):
    def __init__(self,event_engine):
        self._event_engine = event_engine
        self._tick_sock = Socket(SUB)
        self._msg_sock = Socket(PAIR)

        self._active = False
        self._thread = Thread(target=self._run)

    def _run(self):
        while self._active:
            try:
                msg1 = self._tick_sock.recv(flags=1)
                msg1 = msg1.decode("utf-8")
                if msg1 is not None and msg1.index('|') > 0:
                    if msg1[-1] == '\0':
                        msg1 = msg1[:-1]
                    v = msg1.split('|')
                    k = TickEvent()
                    k.full_symbol = v[0]
                    k.price = v[3]

                    self._event_engine.put(k)
            except Exception as e:
                pass
                # print('SUB error: ' + str(e))

            try:
                msg2 = self._msg_sock.recv(flags=1)
                msg2 = msg2.decode("utf-8")
                if msg2 is not None and msg2.index('|') > 0:
                    if msg2[-1] == '\0':
                        msg2 = msg2[:-1]
                    m = GeneralEvent()
                    m.content = msg2

                    self._event_engine.put(m)
            except Exception as e:
                pass
                # print('PAIR error: '+ str(i) + '' + str(e));
                # time.sleep(1)

    def start(self, timer=True):
        """
        start the mq thread
        """
        self._tick_sock.connect('tcp://127.0.0.1:55555')
        self._tick_sock.set_string_option(SUB, SUB_SUBSCRIBE, '')  # receive msg start with all

        self._msg_sock.connect('tcp://127.0.0.1:55558')
        self._active = True

        if not self._thread.isAlive():
            self._thread.start()

    def stop(self):
        """
        stop the mq thread
        """
        self._active = False

        if self._thread.isAlive():
            self._thread.join()