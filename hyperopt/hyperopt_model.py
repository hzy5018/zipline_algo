#!/usr/local/bin/python3
# coding=utf-8
__author__ = 'chiyuen_woo'
# *******************************************************************
#     Filename @  hyperopt_model.py
#       Author @  chiyuen_woo
#  Create date @  2019-04-02 16:44
#        Email @  huzhy5018@gmail.com
#  Description @  邮件发送
#      license @ (C) Copyright 2011-2017, ShuHao Corporation Limited.
# ********************************************************************

import pandas as pd
import numpy as np
import bb_win
import hyperopt.mongoexp

from hyperopt import fmin, tpe, hp, space_eval, pyll, rand, anneal
from hyperopt.mongoexp import MongoTrials

if __name__  == '__main__':
    trials = MongoTrials('mongo://localhost:27018/foo_db/jobs', exp_key='exp2')
    best = fmin(fn=bb_win., space=hyperopt_model.space,  algo=rand.suggest, max_evals=100, trials=trials)
    print best


