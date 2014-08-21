#!/usr/bin/env python 

import subprocess

# Generating plots with lplot are done using python and subprocess. This script
# is used to invoke printenv, to show how subprocess.open with an empty
# environment can possibly affect addresses compared to executing from shell.
# In conclusion, perf stat adds about 170 bytes, including PWD which will
# obviously vary between setups. Launching through subprocess.Popen does not
# affect environment or variable addresses. 

# $ ./printenv.py
# PWD=/home/lars/bias-paper/code/perf-env
# SHLVL=0
# PERF_BUILDID_DIR=.debug
# PATH=/usr/libexec/perf-core:/usr/lib/linux-tools/3.11.0-15-generic:/usr/local/bin:/usr/bin:/bin

p = subprocess.Popen("perf stat -e cycles:u bin/printenv", env={}, shell=True)
p.wait()
