#!/usr/bin/env python 
import sys, argparse, numpy
from scipy import stats

# Calculate linear correlation of lperf formatted performance data. Argument
# matches a mnemonic from input file, typically cycles:u.
# From [name, mnemonic, 0, 1, 2, 3, ...]
# To   [name, mnemonic, correlation, 0, 1, 2, 3, ...]
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('event')
    args = parser.parse_args()

    # Consume and update header
    header = args.input.readline().split(",")
    header.insert(2, "Correlation")
    args.output.write(",".join(header))

    def splitline(line):
        return (line.split(',')[:2], map(int, line.split(',')[2:]))

    # Read all lines as [([name, mnemonic], [counts])]
    events = map(splitline, args.input)

    # Extract counts for event to calculate correlation with
    reference = filter(lambda e: e[0][1] == args.event, events)[0][1]

    # Calculate correlation for all events
    numpy.seterr(invalid='ignore')
    correlations = map(lambda (x): stats.pearsonr(reference, x)[0], map(lambda (x, y): y, events))

    # Output rest
    for ((names, counts), correlation) in zip(events, correlations):
        args.output.write(",".join(map(str, names + [correlation] + counts)))
        args.output.write('\n')
