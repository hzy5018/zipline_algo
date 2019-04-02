#!/usr/local/bin/python3
# coding=utf-8
__author__ = 'chiyuen_woo'
import talib
from zipline import run_algorithm
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
from hyperopt import Trials, fmin, tpe
from hyperopt import hp
import numpy as np
import pandas as pd
import datetime


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
        UseParams = False
        try:
            Nparams = len(context.algo_params)
            if Nparams == 3:
                UseParams = True
            else:
                print('len context.algo_params is', Nparams, ' expecting 3')

        except Exception as e:
            print('context.algo_params not passed')

        if UseParams:
            print('Setting Algo parameters via passed algo_params')
            context.BBANDS_timeperiod = context.algo_params['timeperiod']
            context.BBANDS_nbdevup = context.algo_params['nbdevup']
            context.BBANDS_nbdevdn = context.algo_params['nbdevdn']

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


tpe_trials = Trials()
opt_params = fmin(fn=objective,
                  space=hyper_params_space,
                  algo=tpe.suggest,
                  max_evals=300,
                  trials=tpe_trials,
                  rstate=np.random.RandomState(100))

tpe_results = pd.DataFrame({'score': [x['loss'] for x in tpe_trials.results],
                            'timeperiod': tpe_trials.idxs_vals[1]['timeperiod'],
                            'nbdevup': tpe_trials.idxs_vals[1]['nbdevup'],
                            'nbdevdn': tpe_trials.idxs_vals[1]['nbdevdn']})
tpe_results.sort_values(by=['score'], inplace=True)

print(tpe_results.head(10))
print(opt_params)
