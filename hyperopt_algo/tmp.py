#!/usr/local/bin/python3
# coding=utf-8
__author__ = 'chiyuen_woo'
# *******************************************************************
#     Filename @  tmp.py
#       Author @  chiyuen_woo
#  Create date @  2019-04-02 13:23
#        Email @  huzhy5018@gmail.com
#  Description @  邮件发送
#      license @ (C) Copyright 2011-2017, ShuHao Corporation Limited.
# ********************************************************************

import numpy as np
from hyperopt import hp, tpe, fmin

# Single line bayesian optimization of polynomial function
best = fmin(fn=lambda x: np.poly1d([1, -2, -28, 28, 12, -26, 100])(x),
            space=hp.normal('x', 4.9, 0.5), algo=tpe.suggest,
            max_evals=2000)

print(best)