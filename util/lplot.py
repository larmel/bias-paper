#!/usr/bin/env python
import sys, argparse, string
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.ticker import FuncFormatter, MultipleLocator

# Plotting for quick feedback of perf data generated by lperf. Can be invoked
# by piping from lperf directly. `./lperf -e cycles:u -n 100 true | ./lplot`
def parseargs():
    fmt_millions = FuncFormatter( lambda x, _: '%1d' % (x*1e-6) )
    fmt_commas = FuncFormatter( lambda x, _: '{:0,d}'.format(int(x)) )
    def axis_format(s):
        return fmt_millions if s == 'millions' else fmt_commas

    parser = argparse.ArgumentParser(prog="lplot", description='Plot lperf data')
    parser.add_argument("--input", type=argparse.FileType('r'), default="-")
    parser.add_argument('-e', '--events', default='all')
    parser.add_argument('-t', '--title', default='lplot')
    parser.add_argument('-x', '--xlabel', default='')
    parser.add_argument('-y', '--ylabel', default='')
    parser.add_argument('-d', '--dimension', nargs=2, default=(8, 4), \
        metavar=('width', 'height'), type=float)
    parser.add_argument('-l', '--legend', \
        choices=['upper right', 'upper left', 'lower left', 'lower right', 'right', \
                 'center left', 'center right', 'lower center', 'upper center', 'center'],\
        default='upper right')
    parser.add_argument('--legendcols', type=int, default=1)
    parser.add_argument('--export', type=argparse.FileType('w'), default=None)
    parser.add_argument('--ticks', type=int, default=None)
    parser.add_argument('--ybins', type=int, default=None)
    parser.add_argument('--stride', type=int, default=1)
    parser.add_argument('--ylim', type=int, default=None)
    parser.add_argument('--ytickformat', type=axis_format, default=fmt_commas)
    args = parser.parse_args()
    args.events = map(string.lower, args.events.strip().split(','))
    return args

def plot(args):
    rc('text', usetex=True)
    rc('font', family='serif', serif='Computer Modern Roman', size=10)
    rc('legend', frameon=True, fontsize=10)
    rc('axes', linewidth=0.5, titlesize=10, labelsize=10)
    rc('lines', linewidth=0.5)
    rc('patch', linewidth=0.5)
    rc('figure', facecolor='white', edgecolor='white', \
        figsize=(args.dimension[0],args.dimension[1]))

    plt.figure(args.title)
    plt.xlabel(args.xlabel)
    plt.ylabel(args.ylabel)
    plt.gca().yaxis.set_major_formatter(args.ytickformat)

    if args.ylim != None:
        plt.gca().set_ylim([0,args.ylim])
    if args.ybins != None:
        plt.locator_params(axis = 'y', nbins=args.ybins)
    if args.ticks != None:
        locator = MultipleLocator(args.ticks)
        plt.gca().xaxis.set_major_locator(locator)

    header = args.input.readline().split(",")
    start = 3 if "Correlation" in header else 2
    for line in args.input:
        e = map(lambda s : s.strip(), line.split(','))
        if args.events == ['all'] or e[1].lower() in args.events:
            numbers = map(float, e[start:])
            plt.plot( \
                [args.stride*v for v in range(len(numbers))], \
                numbers, \
                label='{{{e}}}'.format(e=e[0].replace('_', '\_')) \
            )
    
    if args.legend != None:
       plt.legend(loc=args.legend, ncol=args.legendcols).draggable()

    plt.grid(True)
    plt.tight_layout()

    if args.export:
        plt.savefig(args.export)
    else:
        plt.show()

if __name__ == '__main__':
    args  = parseargs()
    plot(args)
