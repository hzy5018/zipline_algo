#!/usr/local/bin/python3
# coding=utf-8
__author__ = 'chiyuen_woo'
# *******************************************************************
#     Filename @  bb_win.py
#       Author @  chiyuen_woo
#  Create date @  2019-04-04 13:23
#        Email @  huzhy5018@gmail.com
#  Description @  邮件发送
#      license @ (C) Copyright 2011-2017, ShuHao Corporation Limited.
# ********************************************************************

# bolling bands for trading.

# from zipline.api import order_optimal_portfolio
from zipline.api import attach_pipeline, pipeline_output
from zipline.api import date_rules
from zipline.api import schedule_function, record, symbol
from zipline.api import time_rules, order_target_percent
from zipline.pipeline import Pipeline
from zipline.pipeline.data import USEquityPricing
from zipline.pipeline.factors.technical import BollingerBands


def initialize(context):
    # Schedule our rebalance function to run at the start of
    # each week, when the market opens.
    # schedule_function(
    #     my_rebalance,
    #     date_rules.week_start(),
    #     time_rules.market_open()
    # )

    # Record variables at the end of each day.
    schedule_function(
        my_record_vars,
        date_rules.every_day(),
        time_rules.market_close()
    )

    # Create our pipeline and attach it to our algorithm.
    my_pipe = make_pipeline(10, 2)
    attach_pipeline(my_pipe, 'my_pipeline')


def make_pipeline(time_period, k):
    """
    Create our pipeline.
    """

    # bolling bands
    BolU, BolM, BolL = BollingerBands(
        inputs=[USEquityPricing.close],
        window_length=time_period,
        k=k
    )

    return Pipeline(
        columns={
            'BolU': BolU,
            'BolM': BolM,
            'BolL': BolL
        },
    )


# def compute_target_weights(context, data):
#     """
#     Compute ordering weights.
#     """
#
#     # Initialize empty target weights dictionary.
#     # This will map securities to their target weight.
#     weights = {}
#
#     # If there are securities in our longs and shorts lists,
#     # compute even target weights for each security.
#     if context.longs and context.shorts:
#         long_weight = 0.5 / len(context.longs)
#         short_weight = -0.5 / len(context.shorts)
#     else:
#         return weights
#
#     # Exit positions in our portfolio if they are not
#     # in our longs or shorts lists.
#     for security in context.portfolio.positions:
#         if security not in context.longs and security not in context.shorts and data.can_trade(
#                 security):
#             weights[security] = 0
#
#     for security in context.longs:
#         weights[security] = long_weight
#
#     for security in context.shorts:
#         weights[security] = short_weight
#
#     return weights


def before_trading_start(context, data):
    """
    Get pipeline results.
    """
    context.secs = [symbol('000001.SZ')]
    pipe_results = pipeline_output('my_pipeline')
    context.BolU = pipe_results["BolU"]
    context.BolL = pipe_results["BolL"]
    context.BolM = pipe_results["BolM"]
    # Gets our pipeline output every day.

    #
    # # Go long in securities for which the 'longs' value is True,
    # # and check if they can be traded.
    # context.longs = []
    # for sec in pipe_results[pipe_results['longs']].index.tolist():
    #     if data.can_trade(sec):
    #         context.longs.append(sec)
    #
    # # Go short in securities for which the 'shorts' value is True,
    # # and check if they can be traded.
    # context.shorts = []
    # for sec in pipe_results[pipe_results['shorts']].index.tolist():
    #     if data.can_trade(sec):
    #         context.shorts.append(sec)


# def my_rebalance(context, data):
#     """
#     Rebalance weekly.
#     """
#
#     # Calculate target weights to rebalance
#     target_weights = compute_target_weights(context, data)
#
#     # If we have target weights, rebalance our portfolio
#     if target_weights:
#         order_optimal_portfolio(
#             objective=opt.TargetWeights(target_weights),
#             constraints=[],
#         )


def my_record_vars(context, data):
    """
    Record variables at the end of each day.
    """

    # longs = shorts = 0
    # for position in context.portfolio.positions.itervalues():
    #     if position.amount > 0:
    #         longs += 1
    #     elif position.amount < 0:
    #         shorts += 1

    # Record our variables.
    S = context.secs[0]
    CurP = data[S].price
    BolL, BolM, BolU = context.BolL, context.BolM, context.BolU
    if CurP < BolL[-1]:
        order_target_percent(S, +0.97)

    elif CurP > BolU[-1]:
        order_target_percent(S, -0.97)
    record(CurP=CurP, BolU=BolU[-1], BolM=BolM[-1], BolL=BolL[-1])

