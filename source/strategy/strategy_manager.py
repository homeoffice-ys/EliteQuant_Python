#!/usr/bin/env python
# -*- coding: utf-8 -*-
class StrategyManager(object):
    def __init__(self, config_client, outgoing_request_event_engine, order_manager, portfolio_manager):
        self._config_client = config_client
        self._outgoing_request_event_engine = outgoing_request_event_engine
        self._order_manager = order_manager    # get sid from
        self._portfolio_manager = portfolio_manager
        self._strategy_id = 1
        self._strategies_dict = {}            # strategy_id ==> strategy
        # there could be more than one strategy that subscribes to a symbol
        self._tick_strategy_dict = {}  # sym -> list of strategy
        self.sid_oid_dict = {}  # sid => list of order id
        self._oid_sid_dict = {}   # oid ==> sid; the opposite of sid_oid_dict
        self.reset()

    def reset(self):
        self._strategy_id = 1          # 0 is mannual discretionary trade
        self.sid_oid_dict.clear()
        self._oid_sid_dict.clear()

    def load_strategy(self, strategy_name):
        strategy = None
        strategy.on_init()
        strategy.register_tick()              # register to tick ===> strat dictionary
        self._strategies_dict[self._strategy_id] = strategy

    def init_strategy(self, sid):
        pass

    def start_strategy(self, sd):
        pass

    def stop_strategy(self, sid):
        pass

    def pause_strategy(self, sid):
        pass

    def flat_strategy(self, sid):
        pass

    def start_all(self):
        pass

    def stop_all(self):
        pass

    def flat_all(self):
        pass

    def cancel_all(self):
        pass

    def send_order(self):
        pass

    def cancel_order(self, o):
        pass

    def on_tick(self, k):
        if k.full_symbol in self._tick_strategy_dict:
            # foreach strategy that subscribes to this tick
            s_list = self._tick_strategy_dict[k.full_symbol]
            for s in s_list:
                s.on_tick(k)

        for s in self._strategies_dict:
            s.on_tick(k)

    def on_position(self, pos):
        pass

    def on_order_status(self, os):
        if os.client_order_id in self._oid_sid_dict:
            self._strategies_dict[os.client_order_id].on_order_status(os)
        else:
            print('strategy manager doesnt hold the oid, possibly from outside of the system')

    def on_cancel(self, oid):
        pass

    def on_fill(self, fill):
        pass