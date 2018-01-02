#!/usr/bin/env python
# -*- coding: utf-8 -*-
class StrategyManager:
    def __int__(self, outgoingqueue):
        self._outgoing_queue = outgoingqueue
        self._strategies = []

    def load_strategy(self, strategy_name):
        strategy = None
        strategy.on_start()
        self._strategies.append(strategy)

    def send_order(self):
        msg = 'o|MKT'

        print('send message:' + msg)
        self._outgoing_queue.put(msg)

    def cancel_order(self, o):
        self._outgoing_queue.put(o)

    def on_tick(self, k):
        for s in self._strategies:
            s.on_tick(k)

    def on_position(self, pos):
        pass

    def on_order(self, o):
        pass

    def on_cancel(self, oid):
        pass

    def on_fill(self, fill):
        pass