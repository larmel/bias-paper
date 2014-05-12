#!/usr/bin/env python
import sys

# Convert output of lperf to a format that is easier to parse for the LaTeX 
# pgfplots package.
#
# From: [name, mnemonic {,correlation}?, a, b, c, ...]
#
# To:     n     cycles:u    r0107:u   ...
#         a        50          8
#         b         6          1
#
# Usage: lperf <args> | pgfconv > output.dat
#
if __name__ == '__main__':
    header = sys.stdin.readline().strip().split(",")
    startidx = 3 if "Correlation" in header else 2
    data = [["n"] + header[startidx:]]
    
    for line in sys.stdin:
        row = line.strip().split(',')
        event, numbers = row[1], row[startidx:]
        data.append([event] + numbers)

    n = len(data[0])
    for i in range(n):
        print '\t'.join(data[k][i] for k in range(len(data)))
