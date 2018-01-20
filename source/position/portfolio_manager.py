#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .position import Position

class PortfolioManager(object):
    def __init__(self, initial_cash):
        """
        PortfolioManager is one component of PortfolioManager
        """
        self.cash = initial_cash
        self.contracts = {}            # symbol ==> contract
        self.positions = {}

    def reset(self):
        self.contracts.clear()
        self.positions.clear()

    def on_contract(self, contract):
        if contract.full_symbol not in self.contracts:
            self.contracts[contract.full_symbol] = contract
            print("Contract %s information received. " % contract.full_symbol)
        else:
            print("Contract %s information already exists " % contract.full_symbol)

    def on_position(self, pos_event):
        """get initial position"""
        pos = pos_event.to_position()

        if pos.full_symbol not in self.positions:
            self.positions[pos.full_symbol] = pos
        else:

            print("Symbol %s already exists in the portfolio " % pos.full_symbol)

    def on_fill(self, fill_event):
        """
        This works only on stocks.
        TODO: consider margin
        """
        # sell will get cash back
        self.cash -= fill_event.fill_size * fill_event.fill_price + fill_event.commission

        if fill_event.full_symbol in self.positions:      # adjust existing position
            self.positions[fill_event.full_symbol].on_fill(fill_event)
        else:
            self.positions[fill_event.full_symbol] = fill_event.to_position()

    def mark_to_market(self, current_time, symbol, last_price):
        #for sym, pos in self.positions.items():
        if symbol in self.positions:
            self.positions[symbol].mark_to_market(last_price)