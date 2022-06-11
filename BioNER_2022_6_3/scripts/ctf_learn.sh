#!/bin/sh
crf_learn  -p 2 -f 3 -c 4.0  template train_file model_2022_6_8
crf_test -v0 - n 20 -m  model.2022.6.6 ../testFormat.txt