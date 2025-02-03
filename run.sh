#!/usr/bin/bash

nohup python test_Dual_Mark.py > out.log 2>&1 &

tail -f out.log