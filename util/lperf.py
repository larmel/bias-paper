#!/usr/bin/env python 
import subprocess, argparse, sys
from perfevents import events

def parseargs():
    def perfctr(s):
        counter = filter(lambda (ctr): ctr.perfcode() == s.lower() or ctr.mnemonic() == s.lower(), events)
        if not counter:
            raise argparse.ArgumentTypeError("Unrecognized event " + s)
        return counter[0]

    def perfctrs(s):
        return events if s == "all" else list(set(map(perfctr, s.strip().lower().split(','))))

    parser = argparse.ArgumentParser(prog="lperf", description='perf wrapper for varying execution contexts')
    parser.add_argument('-e', '--events', type=perfctrs, default="all", help="Comma separated list of event code or mnemonic")
    parser.add_argument('-n', '--iterations', type=int, default=1)
    parser.add_argument('-r', '--repeat', type=int, default=1, help="Average results over multiple runs, using perf-stat -r")
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('--env-offset', type=int, default=0, help="Number of bytes initially added to environment")
    parser.add_argument('--env-increment', type=int, default=1, help="Number of bytes added to environment each iteration")
    parser.add_argument('--enumerate', default=False, action='store_true', help="Supply iteration number as program argument")
    parser.add_argument('program')
    parser.add_argument('arg', nargs=argparse.REMAINDER)
    args = parser.parse_args()

    if args.arg:
        args.program += " " + " ".join(args.arg)
    del args.arg

    return args

def benchmark(args):
    counters = args.events
    data = { counter: {'count': [0] * args.iterations } for counter in args.events }

    # Measure all counters under n different environments
    for x in range(args.iterations):
        argument = "" if not args.enumerate else str(x)
        env = {'X': '0' * (args.env_offset + x*args.env_increment)}

        # Sample at most 4 events at a time because of register limitations
        for i in range(0, len(counters), 4):
            current = counters[i:i + 4]

            prfevnt = ','.join(map(lambda (c): c.mnemonic(), current))
            command = ' '.join(["perf stat -r", str(args.repeat), '-x"," -e', prfevnt, args.program, argument])
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, shell=True)

            for counter in current:
                data[counter]['count'][x] = int(process.stderr.readline().strip().split(',')[0])

            for line in process.stdout:
                sys.stderr.write(line)

            process.wait()

    return data

if __name__ == '__main__':
    args = parseargs()
    data = benchmark(args)

    args.output.write("Performance counter,Mnemonic,")
    args.output.write(",".join(map(str, range(args.iterations))) + "\n")

    for event in args.events:
        row = [event.name, event.mnemonic()] + data[event]['count']
        args.output.write(",".join(map(str, row)) + "\n")
