# encoding: UTF-8
from __future__ import print_function

from .position import Position

class PortfolioManager(object):
    def __init__(self, initial_cash):
        """
        PortfolioManager is one component of PortfolioManager
        """
        self.cash = initial_cash
        self.positions = {}

    def on_position(self, symbol, price, quantity, commission=0.0):
        """get initial position"""
        position = Position(symbol, price, quantity)

        if position.full_symbol not in self.positions:
            self.positions[position.full_symbol] = position
        else:
            print("Symbol %s already exists in the portfolio " % position.full_symbol)

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