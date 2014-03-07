#!/usr/bin/env python 
import sys, argparse, numpy
from matplotlib import pyplot as plt, ticker

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=argparse.FileType('r'), default="-")
    parser.add_argument('--export', type=argparse.FileType('w'), default=None)
    args = parser.parse_args()

    matrix = numpy.loadtxt(args.input, delimiter=",", dtype=int)

    y, x = matrix.shape

    plt.xlabel("x vector address offset times 0x010")
    plt.ylabel("y vector address offset times 0x010")

    plt.xlim(0, x)
    plt.ylim(0, y)

    plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    plt.title("Estimated cost of dgemv")
    plt.pcolor(matrix)
    plt.colorbar()
    if args.export:
        plt.savefig(args.export)
    plt.show()
