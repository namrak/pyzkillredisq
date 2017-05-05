#!/bin/bash

# shell script to start gathering killmails via crontab
# recommend a line similar to the following to run every hour:
# 00 * * * * env DISPLAY=:0 /usr/bin/xterm -e /home/<username>/pyzkillredisq/getkills/crongetkills.sh
cd /home/<username>/pyzkillredisq/
python3.6 getkills/getkills.py