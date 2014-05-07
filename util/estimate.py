#!/usr/bin/env python 
import sys, argparse, numpy

# Calculate the estimated cost of a program when subtracting constant overhead.
# Input is two performance measurement sets, t_few and t_many. Estimation is
# t_estimate = (t_few - t_many) / (many - few). 
# Input can optionally contain correlation [name, mnemonic, correlation, 0, 1, 2, 3, ...]
# Output removes correlation
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--longrun', type=argparse.FileType('r'))
    parser.add_argument('--shortrun', type=argparse.FileType('r'))
    parser.add_argument('-o', '--outfile', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-r', '--delta', type=int, default=1)
    args = parser.parse_args()

    # Propagate header, discarding correlation
    args.shortrun.readline()
    args.outfile.write(args.longrun.readline().replace("Correlation,",""))

    # Split into ([name, mnemonic], [values])
    def splitline(line):
        tokens = line.replace("Correlation,","").split(",")
        return (tokens[:2], map(int, tokens[2:]))

    # Calculate estimate counter value based on two series
    def diffline(onerun, manyruns, howmany):
        return map(lambda (one, many): (many - one) // howmany, zip(onerun, manyruns))

    # Read files in parallel and output estimate
    for x, y in zip(args.shortrun, args.longrun):
        header, onecount = splitline(x)
        _, manycounts = splitline(y)
        args.outfile.write(','.join(header + map(str, diffline(onecount, manycounts, args.delta))))
        args.outfile.write('\n')
