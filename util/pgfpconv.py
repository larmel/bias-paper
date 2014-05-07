#!/usr/bin/env python
import sys

# Convert output of lperf to a format that is easier to parse for the LaTeX 
# pgfplots package.
#
# From: [name, mnemonic {,correlation}?, 0, 1, 2, ...]
#
# To:     n     cycles:u    r0107:u   ...
#         0        50          8
#         1         6          1
#
# Usage: lperf <args> | pgfconv > output.dat
#
if __name__ == '__main__':
    data = [[]]
    header = sys.stdin.readline()
    startidx = header.split(',').index('0')
    
    for line in sys.stdin:
        row = line.strip().split(',')
        event, numbers = row[1], row[startidx:]
        data.append([event] + numbers)

    n = len(data[1])
    data[0] = ["n"] + map(str, range(0, n - 1))
    for i in range(n):
        print '\t'.join(data[k][i] for k in range(len(data)))
