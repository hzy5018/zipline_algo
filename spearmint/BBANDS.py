#!/usr/local/bin/python3
# coding=utf-8
__author__ = 'chiyuen_woo'
# *******************************************************************
#     Filename @  BBANDS.py.py
#       Author @  chiyuen_woo
#  Create date @  2019-04-01 17:29
#        Email @  huzhy5018@gmail.com
#  Description @  邮件发送
#      license @ (C) Copyright 2011-2017, ShuHao Corporation Limited.
# ********************************************************************

# !/usr/bin/python
import sys
from zipline import run_algorithm


def main(job_id, D):
    parsed = {'symbols': 'SPY', 'start': '2014-01-01', 'end': '2014-12-31',
              'algofile': '/home/quant/pta/py/algos/BBANDS-zipday.py',
              'capital_base': '100000', 'data_frequency': 'daily',
              'conf_file': None, 'source': 'yahoo', 'output': None,
              'risk': None, 'algo_params': D}

    # Below what we expect spearmint to pass us
    # parsed['algo_params']=[47,88.7,7.7]
    # D={}
    # D['timeperiod']=10
    # D['nbdevup']=1.00
    # D['nbdevdn']=1.00

    perf = run_algorithm(**parsed)

    StartV = perf['portfolio_value'][0]

    EndV = perf['portfolio_value'][-1]

    # spearmint wants to minimize so return negative profit
    BBANDS = (StartV - EndV)

    return BBANDS


if __name__ == "__main__":
    # Below will be overridden by spearmint when it runs
    main(47, {'timeperiod': 10, 'nbdevup': 1.00, 'nbdevdn': 1.00})
