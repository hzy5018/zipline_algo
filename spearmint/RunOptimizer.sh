#!/bin/bash
HOMX=/home/quant
cd $HOMX/spearmint-master/spearmint/bin
./spearmint -w                  \
   ../examples/BBANDS/config.pb \
   --driver=local               \
   --port=9999                  \
   --max-concurrent=3           \
   --method=RandomChooser      \
   --method-args=noiseless=1
exit