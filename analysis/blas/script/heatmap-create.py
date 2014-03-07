#!/usr/bin/env python 
import sys, argparse, subprocess, numpy

def command(prog, counter, dx, dy, iterations):
    return "perf stat -r 5 -x ',' -e %s %s %s %s %s > /dev/null" % (counter, prog, dx, dy, iterations)

def run(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env={}, shell=True)
    value = int(process.stderr.readline().strip().split(',')[0])
    process.wait()
    return value

def sample(prog, counter, dx, dy):
    cmd_101 = command(prog, counter, dx, dy, 101)
    cmd_1   = command(prog, counter, dx, dy, 1)
    return (run(cmd_101) - run(cmd_1)) / 100

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("program")
    parser.add_argument("-e", "--counter", default="r0107:u")
    parser.add_argument("-x", type=int, default=32)
    parser.add_argument("-y", type=int, default=32)
    args = parser.parse_args()

    heatmap = [[0]*args.x for i in range(args.y)]

    # Malloc allocates in multiples of 16 B, sample suffixes 0x000, 0x010, 0x020, etc. To
    # cover all possibilities for vectors x and y, number of buckets should be 4096/16 = 256.
    for y in range(args.y):
        for x in range(args.x):
            heatmap[y][x]  = sample(args.program, args.counter, x*16, y*16)

    numpy.savetxt(sys.stdout, numpy.asarray(heatmap), fmt='%s', delimiter=',')
