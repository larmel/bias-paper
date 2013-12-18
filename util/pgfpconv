#!/usr/bin/env python
import sys

#
# Script to convert output of lperf to a format that is easier to parse for
# the LaTeX pgfplots package. 
# Usage: lperf <args> | pgfconv > output.dat

if __name__ == '__main__':
	data = [[]]
	for line in sys.stdin:
		if line[0] == '#':
			sys.stdout.write(line)
		else:
			row = line.strip().split(',')
			header, numbers = row[1], row[3:]
			data.append([header] + numbers)

	n = len(data[1])
	data[0] = ["n"] + map(str, range(0, n - 1))
	for i in range(n):
		print '\t'.join(data[k][i] for k in range(len(data)))
