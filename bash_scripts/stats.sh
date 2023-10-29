#!/usr/bin/env bash

pwd; hostname; date

source activate RL_breaking_U3T

python ./play_modes/stats.py &> output

date