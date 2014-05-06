#!/usr/bin/env python 
import sys, argparse, numpy

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--longrun', type=argparse.FileType('r'))
    parser.add_argument('--shortrun', type=argparse.FileType('r'))
    parser.add_argument('-o', '--outfile', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-r', '--delta', type=int, default=1)
    args = parser.parse_args()

    # Propagate header
    args.shortrun.readline()
    args.outfile.write(args.longrun.readline())

    # Split into ([name, mnemonic], [values]), discard correlation
    # TODO: Check if correlation is there... BUGS CURRENTLY!
    def splitline(line):
        return (line.split(',')[:2], map(int, line.split(',')[3:]))

    # Calculate estimate counter value based on two series
    def diffline(onerun, manyruns, howmany):
        return map(lambda (one, many): (many - one) // howmany, zip(onerun, manyruns))

    # Read files in parallel and output estimate
    for x, y in zip(args.shortrun, args.longrun):
        header, onecount = splitline(x)
        _, manycounts = splitline(y)
        args.outfile.write(','.join(header + map(str, diffline(onecount, manycounts, args.delta))))
        args.outfile.write('\n')
