#!/usr/bin/env python 
import sys, subprocess, numpy
from matplotlib import pyplot as plt

prog = "bin/gemv-grid"

def command(counter, dx, dy, iterations):
    return "perf stat -r 5 -x ',' -e %s %s %s %s %s > /dev/null" % (counter, prog, dx, dy, iterations)

def run(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env={}, shell=True)
    value = int(process.stderr.readline().strip().split(',')[0])
    process.wait()
    return value

def sample(counter, dx, dy):
    return (run(command(counter, dx, dy, 101)) - run(command(counter, dx, dy, 1))) / 100

if __name__ == '__main__':

    # malloc allocates in multiples of 16, so the max sensible number of 
    # buckets would be 4096 / 16 = 256, sampling 0x10, 0x20, etc.
    nx = 256
    ny = 256

    # Offset in bytes each sample
    dx = 16 #(4096) / nx
    dy = 16 #(4096) / ny

    alias  = [[0]*nx for i in range(ny)]

    for y in range(ny):
        for x in range(nx):
            alias[y][x]  = sample("r0107:u", x*dx, y*dy)

    matrix = numpy.asarray(alias)
    numpy.savetxt(sys.stdout, matrix, fmt='%s', delimiter=',')

    heatmap = plt.pcolor(matrix)
    plt.savefig('bin/heatmap-alias.png')
    plt.show()

