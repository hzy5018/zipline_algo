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

import numpy as np
import pandas as pd
from hyperopt import fmin, tpe
from hyperopt.mongoexp import MongoTrials

from hyperopt_algo.bb_win import objective, hyper_params_space

if __name__ == '__main__':
    tpe_trials = MongoTrials('mongo://localhost:27018/foo_db/jobs',
                             exp_key='exp1')
    opt_params = fmin(fn=objective,
                      space=hyper_params_space,
                      algo=tpe.suggest,
                      max_evals=300,
                      trials=tpe_trials,
                      rstate=np.random.RandomState(100))
    tpe_results = pd.DataFrame(
        {'score': [x['loss'] for x in tpe_trials.results],
         'timeperiod': tpe_trials.idxs_vals[1]['timeperiod'],
         'nbdevup': tpe_trials.idxs_vals[1]['nbdevup'],
         'nbdevdn': tpe_trials.idxs_vals[1]['nbdevdn']})
    tpe_results.sort_values(by=['score'], inplace=True)

    print(tpe_results.head(10))
    print(opt_params)



