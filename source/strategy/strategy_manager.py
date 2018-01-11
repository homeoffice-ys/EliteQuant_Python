#!/usr/bin/env python
# -*- coding: utf-8 -*-
class StrategyManager:
    def __int__(self, client_config, event_engine, order_manager):
        self._client_config = client_config
        self._event_engine = event_engine
        self._order_manager = order_manager
        self._strategy_id = 1
        self._strategies = []
        self.reset()

    def reset(self):
        self._strategy_id = 1          # 0 is mannual discretionary trade
        self._strategies = []

    def load_strategy(self, strategy_name):
        strategy = None
        strategy.on_init()
        self._strategies.append(strategy)

    def send_order(self):
        pass

    def cancel_order(self, o):
        pass

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