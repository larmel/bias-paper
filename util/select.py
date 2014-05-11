#!/usr/bin/env python 
import sys, argparse, numpy

# Filter rows matching perf counter mnemonic
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=argparse.FileType("r"), default=sys.stdin)
    parser.add_argument("-o", "--output", type=argparse.FileType("w"), default=sys.stdout)
    parser.add_argument("-e", "--events")
    args = parser.parse_args()

    events = args.events.split(",")

    args.output.write(args.input.readline())

    for row in args.input:
        if row.split(",")[1] in events:
            args.output.write(row)
