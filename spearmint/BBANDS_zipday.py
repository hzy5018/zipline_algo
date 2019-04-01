#!/usr/local/bin/python3
# coding=utf-8
__author__ = 'chiyuen_woo'
# *******************************************************************
#     Filename @  BBANDS_zipday.py.py
#       Author @  chiyuen_woo
#  Create date @  2019-04-01 17:29
#        Email @  huzhy5018@gmail.com
#  Description @  邮件发送
#      license @ (C) Copyright 2011-2017, ShuHao Corporation Limited.
# ********************************************************************


from zipline.api import (history,

                         order_target_percent,

                         record,

                         symbol)

import talib


def initialize(context):
    context.secs = [symbol('000001.SZ')]

    context.history_depth = 30

    context.iwarmup = 0

    # add_history(30, '1d', 'price')

    context.BBANDS_timeperiod = 16

    context.BBANDS_nbdevup = 1.819

    context.BBANDS_nbdevdn = 1.470

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

    else:

        if CurP > BolU[-1]:
            order_target_percent(S, -0.97)

    return
