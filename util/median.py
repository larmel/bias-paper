#!/usr/bin/env python 
import sys, argparse, numpy

# Calculate median value of each counter
#
# From [name, mnemonic, [correlation], 0, 1, 2, 3, ...]
# To   [name, mnemonic, median]
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), default=sys.stdout)
    args = parser.parse_args()

    # Consume and update header
    header = args.input.readline().split(",")
    start = header.index("0")
    args.output.write(",".join(header[:2] + ["Median\n"]))

    def transform(line):
        return line.split(',')[:2] + [int(numpy.median(map(int, line.split(',')[start:])))]

    # Read all lines as [[name, mnemonic, median]]
    for row in map(transform, args.input):
        args.output.write(",".join(map(str, row)) + "\n")
