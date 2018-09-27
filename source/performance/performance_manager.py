#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import re
import empyrical as ep
import pyfolio as pf

class PerformanceManager(object):
    """
    Record equity, positions, and trades in accordance to pyfolio format
    First date will be the first data start date
    """
    def __init__(self, symbols, benchmark=None, batch_tag='0', multi=1, fvp=None):
        self._symbols = []
        self._benchmark = benchmark
        self._batch_tag = batch_tag
        self._multi = multi                      # root multiplier, for CL1, CL2
        if multi is None:
            self._multi = 1
        self._df_fvp = fvp

        if self._multi > 1:
            for sym in symbols:
                self._symbols.extend([sym+str(i+1) for i in range(multi)])           # CL1 CL2
        else:
            self._symbols.extend(symbols)

        self._slippage = 0.0
        self._commission_rate = 0.0
        self.reset()

    # ------------------------------------ public functions -----------------------------#
    #  or each sid
    def reset(self):
        self._realized_pnl = 0.0
        self._unrealized_pnl = 0.0

        self._equity = pd.Series()      # equity line
        self._equity.name = 'total'

        if self._multi > 1:
            self._df_positions = pd.DataFrame(columns=self._symbols * 2 + ['cash', 'total', 'benchmark'])  # Position + Symbol
        else:
            self._df_positions = pd.DataFrame(columns=self._symbols + ['cash', 'total', 'benchmark'])   # Position + Symbol

        self._df_trades = pd.DataFrame(columns=['amount', 'price', 'symbol'])

    def set_splippage(self, slippage):
        self._slippage = slippage

    def set_commission_rate(self, commission_rate):
        self._commission_rate = commission_rate

    def update_performance(self, current_time, position_manager, data_board):
        if self._equity.empty:
            self._equity[current_time] = 0.0
            return
        # on a new time/date, calculate the performances for the last date
        elif current_time != self._equity.index[-1]:
            performance_time = self._equity.index[-1]

            equity = 0.0
            self._df_positions.loc[performance_time] = [0] * len(self._df_positions.columns)
            for sym, pos in position_manager.positions.items():
                m = 1
                if self._df_fvp is not None:
                    try:
                        if '|' in sym:
                            ss = sym.split('|')
                            match = re.match(r"([a-z ]+)([0-9]+)?", ss[0], re.I)
                            sym2 = match.groups()[0]

                        m = self._df_fvp.loc[sym2, 'FVP']
                    except:
                        m = 1

                equity += pos.size * data_board.get_last_price(sym) * m
                if '|' in sym:
                    ss = sym.split('|')
                    self._df_positions.loc[performance_time, ss[0]] = [pos.size * data_board.get_last_price(sym)*m, ss[1]]
                else:
                    self._df_positions.loc[performance_time, sym] = pos.size * data_board.get_last_price(sym) * m
            self._df_positions.loc[performance_time, 'cash'] = position_manager.cash
            self._equity[performance_time] = equity + position_manager.cash
            self._df_positions.loc[performance_time, 'total'] = self._equity[performance_time]
            # calculate benchmark
            if self._benchmark is not None:
                if self._df_positions.shape[0] == 1:
                    self._df_positions.at[performance_time, 'benchmark'] = self._equity[performance_time]
                else:
                    benchmark_p0 = data_board.get_hist_price(self._benchmark, performance_time)
                    periodic_ret = 0
                    try:
                        periodic_ret = benchmark_p0.iloc[-1]['Close'] / benchmark_p0.iloc[-2]['Close'] - 1
                    except:
                        periodic_ret = benchmark_p0.iloc[-1]['Price'] / benchmark_p0.iloc[-2]['Price'] - 1
                    self._df_positions.at[performance_time, 'benchmark'] = self._df_positions.iloc[-2]['benchmark'] * (
                                1 + periodic_ret)

            self._equity[current_time] = 0.0

    def on_fill(self, fill_event):
        # self._df_trades.loc[fill_event.timestamp] = [fill_event.fill_size, fill_event.fill_price, fill_event.full_symbol]
        self._df_trades = self._df_trades.append(pd.DataFrame(
            {'amount': [fill_event.fill_size], 'price': [fill_event.fill_price], 'symbol': [fill_event.full_symbol]},
            index=[fill_event.fill_time]))

    def update_final_performance(self, current_time, position_manager, data_board):
        """
        When a new data date comes in, it calcuates performances for the previous day
        This leaves the last date not updated.
        So we call the update explicitly
        """
        performance_time = current_time

        equity = 0.0
        self._df_positions.loc[performance_time] = [0] * len(self._df_positions.columns)
        for sym, pos in position_manager.positions.items():
            m = 1
            if self._df_fvp is not None:
                try:
                    if '|' in sym:
                        ss = sym.split('|')
                        match = re.match(r"([a-z ]+)([0-9]+)?", ss[0], re.I)
                        sym2 = match.groups()[0]

                    m = self._df_fvp.loc[sym2, 'FVP']
                except:
                    m = 1
            equity += pos.size * data_board.get_last_price(sym) * m
            if '|' in sym:
                ss = sym.split('|')
                self._df_positions.loc[performance_time, ss[0]] = [pos.size * data_board.get_last_price(sym) * m, ss[1]]
            else:
                self._df_positions.loc[performance_time, sym] = pos.size * data_board.get_last_price(sym) * m
        self._df_positions.loc[performance_time, 'cash'] = position_manager.cash

        self._equity[performance_time] = equity + position_manager.cash
        self._df_positions.loc[performance_time, 'total'] = self._equity[performance_time]

        # calculate benchmark
        if self._benchmark is not None:
            if self._df_positions.shape[0] == 1:
                self._df_positions.at[performance_time, 'benchmark'] = self._equity[performance_time]
            else:
                benchmark_p0 = data_board.get_hist_price(self._benchmark, performance_time)
                periodic_ret = 0
                try:
                    periodic_ret = benchmark_p0.iloc[-1]['Close'] / benchmark_p0.iloc[-2]['Close'] - 1
                except:
                    periodic_ret = benchmark_p0.iloc[-1]['Price'] / benchmark_p0.iloc[-2]['Price'] - 1

                self._df_positions.at[performance_time, 'benchmark'] = self._df_positions.iloc[-2]['benchmark'] * (
                        1 + periodic_ret)

    def caculate_performance(self):
        # to daily
        try:
            rets = self._equity.resample('D').last().dropna().pct_change()
            if self._benchmark is not None:
                b_rets = self._df_positions['benchmark'].resample('D').last().dropna().pct_change()
        except:
            rets = self._equity.pct_change()
            if self._benchmark is not None:
                b_rets = self._df_positions['benchmark'].pct_change()

        rets = rets[1:]
        if self._benchmark is not None:
            b_rets = b_rets[1:]
        perf_stats_all = None
        #rets.index = rets.index.tz_localize('UTC')
        #self._df_positions.index = self._df_positions.index.tz_localize('UTC')
        if not self._df_trades.index.empty:
            if self._benchmark is not None:
                # self._df_trades.index = self._df_trades.index.tz_localize('UTC')
                # pf.create_full_tear_sheet(rets, self._df_positions, self._df_trades)
                rets.index = pd.to_datetime(rets.index)
                b_rets.index = rets.index
                # pf.create_returns_tear_sheet(rets,benchmark_rets=b_rets)
                perf_stats_strat = pf.timeseries.perf_stats(rets)
                perf_stats_benchmark = pf.timeseries.perf_stats(b_rets)
                perf_stats_all = pd.concat([perf_stats_strat, perf_stats_benchmark], axis=1)
                perf_stats_all.columns = ['Strategy', 'Benchmark']
            else:
                # self._df_trades.index = self._df_trades.index.tz_localize('UTC')
                # pf.create_full_tear_sheet(rets, self._df_positions, self._df_trades)
                rets.index = pd.to_datetime(rets.index)
                # pf.create_returns_tear_sheet(rets,benchmark_rets=rets)
                perf_stats_all = pf.timeseries.perf_stats(rets)
                perf_stats_all = perf_stats_all.to_frame(name='Strategy')

        drawdown_df = pf.timeseries.gen_drawdown_table(rets, top=5)
        monthly_ret_table = ep.aggregate_returns(rets, 'monthly')
        monthly_ret_table = monthly_ret_table.unstack().round(3)
        ann_ret_df = pd.DataFrame(ep.aggregate_returns(rets, 'yearly'))
        ann_ret_df = ann_ret_df.unstack().round(3)
        return perf_stats_all, drawdown_df, monthly_ret_table, ann_ret_df

    def create_tearsheet(self):
        # to daily
        try:
            rets = self._equity.resample('D').last().dropna().pct_change()
            if self._benchmark is not None:
                b_rets = self._df_positions['benchmark'].resample('D').last().dropna().pct_change()
        except:
            rets = self._equity.pct_change()
            if self._benchmark is not None:
                b_rets = self._df_positions['benchmark'].pct_change()

        rets = rets[1:]
        if self._benchmark is not None:
            b_rets = b_rets[1:]
        #rets.index = rets.index.tz_localize('UTC')
        #self._df_positions.index = self._df_positions.index.tz_localize('UTC')
        if not self._df_trades.index.empty:
            if self._benchmark is not None:
                # self._df_trades.index = self._df_trades.index.tz_localize('UTC')
                # pf.create_full_tear_sheet(rets, self._df_positions, self._df_trades)
                rets.index = pd.to_datetime(rets.index)
                b_rets.index = rets.index
                pf.create_returns_tear_sheet(rets)
                #pf.create_simple_tear_sheet(rets, benchmark_rets=b_rets)
            else:
                # self._df_trades.index = self._df_trades.index.tz_localize('UTC')
                # pf.create_full_tear_sheet(rets, self._df_positions, self._df_trades)
                rets.index = pd.to_datetime(rets.index)
                pf.create_returns_tear_sheet(rets)
                # pf.create_simple_tear_sheet(rets)

    def save_results(self, output_dir):
        '''
        equity and df_posiiton should have the same datetime index
        :param output_dir:
        :return:
        '''
        self._df_positions = self._df_positions[self._symbols+['cash', 'total', 'benchmark']]
        self._df_positions.to_csv('{}{}{}{}'.format(output_dir, '/positions_', self._batch_tag if self._batch_tag else '', '.csv'))
        self._df_trades.to_csv('{}{}{}{}'.format(output_dir, '/trades_', self._batch_tag if self._batch_tag else '', '.csv'))
    # ------------------------------- end of public functions -----------------------------#