#!/usr/local/bin/python3
# coding=utf-8
__author__ = 'chiyuen_woo'
import numpy as np
import pandas as pd
import talib
from hyperopt import fmin, tpe
from hyperopt import hp
from hyperopt.mongoexp import MongoTrials
from hyperopt import mongoexp
from zipline import run_algorithm
import logging
import sys
# *******************************************************************
#     Filename @  bb_win.py
#       Author @  chiyuen_woo
#  Create date @  2019-04-02 13:27
#        Email @  huzhy5018@gmail.com
#  Description @  邮件发送
#      license @ (C) Copyright 2011-2017, ShuHao Corporation Limited.
# ********************************************************************
from zipline.api import (
    history,

    order_target_percent,

    record,

    symbol)
from multiprocessing import Pool, Process


def score_func(params):
    # # Function for Renko brick optimization
    # def evaluate_renko(brick, history, column_name):
    #     renko_obj = pyrenko.renko()
    #     renko_obj.set_brick_size(brick_size=brick, auto=False)
    #     renko_obj.build_history(prices=history)
    #     return renko_obj.evaluate()[column_name]

    def initialize(context):
        context.secs = [symbol('000001.SZ')]
        context.history_depth = 30
        context.iwarmup = 0
        #     add_history(30, '1d', 'price')
        # context.BBANDS_timeperiod = 16
        # context.BBANDS_nbdevup = 1.819
        # context.BBANDS_nbdevdn = 1.470
        context.BBANDS_timeperiod = params['timeperiod']
        context.BBANDS_nbdevup = params['nbdevup']
        context.BBANDS_nbdevdn = params['nbdevdn']

    def handle_data(context, data):
        context.iwarmup = context.iwarmup + 1

        if context.iwarmup <= (context.history_depth + 1):
            return

        dfHistD = history(30, '1d', 'price')

        S = context.secs[0]

        CurP = data[S].price
        BolU, BolM, BolL = talib.BBANDS(

            dfHistD[S].values,

            timeperiod=context.BBANDS_timeperiod,

            nbdevup=context.BBANDS_nbdevup,

            nbdevdn=context.BBANDS_nbdevdn,

            matype=0)

        record(CurP=CurP, BolU=BolU[-1], BolM=BolM[-1], BolL=BolL[-1])

        if CurP < BolL[-1]:

            order_target_percent(S, +0.97)

        elif CurP > BolU[-1]:
            order_target_percent(S, -0.97)

        return

    def analyze(context, perf):
        pass

    # Run alfo and get the performance

    perf = run_algorithm(
        capital_base=1000000,
        data_frequency='daily',
        bundle='mongo',
        initialize=initialize,
        handle_data=handle_data,
        analyze=analyze,
        start=pd.to_datetime("2014-01-01", utc=True),
        end=pd.to_datetime("2014-12-31", utc=True))

    # Invert the metric

    if pd.isnull(perf.sortino[-1]):
        return 0.0
    else:
        return (-1.0) * perf.sortino[-1]


hyper_params_space = {'timeperiod': hp.uniform('timeperiod', 10, 25),
                      'nbdevup': hp.uniform('nbdevup', 0.5, 2.5),
                      'nbdevdn': hp.uniform('nbdevdn', 0.5, 2.5)}


def weighted_mean(values):
    return np.average(values, weights=list(range(1, len(values) + 1)))


def objective(hyper_params):
    result = score_func(hyper_params)
    return result


# def task2():
#
#
#
# def task1():
#     logging.basicConfig(stream=sys.stderr, level=logging.INFO)
#     print('task1 running')
#     sys.exit(mongoexp.main_worker())


