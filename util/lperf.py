#!/usr/bin/env python 
import subprocess, argparse, sys, numpy, datetime
from collections import namedtuple
from scipy import stats

Counter = namedtuple('Counter', ['mnemonic', 'name'])

# See performance-counters.ods for full reference. Only support user-mode flag
# selected, could be made more generic.
haswell = [Counter(code if mnemonic == "" else mnemonic, name) for code, mnemonic, name in [
    ("r0203:u", "", "LD_BLOCKS.STORE_FORWARD"),
    ("r0803:u", "", "LD_BLOCKS.NO_SR"),
    ("r0105:u", "", "MISALIGN_MEM_REF.LOADS"),
    ("r0205:u", "", "MISALIGN_MEM_REF.STORES"),
    ("r0107:u", "", "LD_BLOCKS_PARTIAL.ADDRESS_ALIAS"),
    ("r0108:u", "", "DTLB_LOAD_MISSES.MISS_CAUSES_A_WALK"),
    ("r0208:u", "", "DTLB_LOAD_MISSES.WALK_COMPLETED_4K"),
    ("r0408:u", "", "DTLB_LOAD_MISSES.WALK_COMPLETED_2M_4M"),
    ("r0e08:u", "", "DTLB_LOAD_MISSES.WALK_COMPLETED"),
    ("r1008:u", "", "DTLB_LOAD_MISSES.WALK_DURATION"),
    ("r2008:u", "", "DTLB_LOAD_MISSES.STLB_HIT_4K"),
    ("r4008:u", "", "DTLB_LOAD_MISSES.STLB_HIT_2M"),
    ("r6008:u", "", "DTLB_LOAD_MISSES.STLB_HIT"),
    ("r8008:u", "", "DTLB_LOAD_MISSES.PDE_CACHE_MISS"),
    ("r030d:u", "", "INT_MISC.RECOVERY_CYCLES"),
    ("r010e:u", "", "UOPS_ISSUED.ANY"),
    ("r100e:u", "", "UOPS_ISSUED.FLAGS_MERGE"),
    ("r200e:u", "", "UOPS_ISSUED.SLOW_LEA"),
    ("r400e:u", "", "UOPS_ISSUED.SiNGLE_MUL"),
    ("r2124:u", "", "L2_RQSTS.DEMAND_DATA_RD_MISS"),
    ("r4124:u", "", "L2_RQSTS.DEMAND_DATA_RD_HIT"),
    ("re124:u", "", "L2_RQSTS.ALL_DEMAND_DATA_RD"),
    ("r4224:u", "", "L2_RQSTS.RFO_HIT"),
    ("r2224:u", "", "L2_RQSTS.RFO_MISS"),
    ("re224:u", "", "L2_RQSTS.ALL_RFO"),
    ("r4424:u", "", "L2_RQSTS.CODE_RD_HIT"),
    ("r2424:u", "", "L2_RQSTS.CODE_RD_MISS"),
    ("r2724:u", "", "L2_RQSTS.ALL_DEMAND_MISS"),
    ("re724:u", "", "L2_RQSTS.ALL_DEMAND_REFERENCES"),
    ("re424:u", "", "L2_RQSTS.ALL_CODE_RD"),
    ("r5024:u", "", "L2_RQSTS.L2_PF_HIT"),
    ("r3024:u", "", "L2_RQSTS.L2_PF_MISS"),
    ("rf824:u", "", "L2_RQSTS.ALL_PF"),
    ("r3f24:u", "", "L2_RQSTS.MISS"),
    ("rff24:u", "", "L2_RQSTS.REFERENCES"),
    ("r5027:u", "", "L2_DEMAND_RQSTS.WB_HIT"),
    ("r4f2e:u", "cache-references:u", "LONGEST_LAT_CACHE.REFERENCE"),
    ("r412e:u", "cache-misses:u", "LONGEST_LAT_CACHE.MISS"),
    ("r003c:u", "cycles:u", "CPU_CLK_UNHALTED.THREAD_P"),
    ("r013c:u", "bus-cycles:u", "CPU_CLK_THREAD_UNHALTED.REF_XCLK"),
    ("r0148:u", "", "L1D_PEND_MISS.PENDING"),
    ("r0149:u", "", "DTLB_STORE_MISSES.MISS_CAUSES_A_WALK"),
    ("r0249:u", "", "DTLB_STORE_MISSES.WALK_COMPLETED_4K"),
    ("r0449:u", "", "DTLB_STORE_MISSES.WALK_COMPLETED_2M_4M"),
    ("r0e49:u", "", "DTLB_STORE_MISSES.WALK_COMPLETED"),
    ("r1049:u", "", "DTLB_STORE_MISSES.WALK_DURATION"),
    ("r2049:u", "", "DTLB_STORE_MISSES.STLB_HIT_4K"),
    ("r4049:u", "", "DTLB_STORE_MISSES.STLB_HIT_2M"),
    ("r6049:u", "", "DTLB_STORE_MISSES.STLB_HIT"),
    ("r8049:u", "", "DTLB_STORE_MISSES.PDE_CACHE_MISS"),
    ("r014c:u", "", "LOAD_HIT_PRE.SW_PF"),
    ("r024c:u", "", "LOAD_HIT_PRE.HW_PF"),
    ("r0151:u", "", "L1D.REPLACEMENT"),
    ("r0458:u", "", "MOVE_ELIMINATION.INT_NOT_ELIMINATED"),
    ("r0858:u", "", "MOVE_ELIMINATION.SIMD_NOT_ELIMINATED"),
    ("r0158:u", "", "MOVE_ELIMINATION.INT_ELIMINATED"),
    ("r0258:u", "", "MOVE_ELIMINATION.SIMD_ELIMINATED"),
    ("r015c:u", "", "CPL_CYCLES.RING0"),
    ("r025c:u", "", "CPL_CYCLES.RING123"),
    ("r015e:u", "", "RS_EVENTS.EMPTY_CYCLES"),
    ("r0160:u", "", "OFFCORE_REQUESTS_OUTSTANDING.DEMAND_DATA_RD"),
    ("r0260:u", "", "OFFCORE_REQUESTS_OUTSTANDING.DEMAND_CODE_RD"),
    ("r0460:u", "", "OFFCORE_REQUESTS_OUTSTANDING.DEMAND_RFO"),
    ("r0860:u", "", "OFFCORE_REQUESTS_OUTSTANDING.ALL_DATA_RD"),
    ("r0163:u", "", "LOCK_CYCLES.SPLIT_LOCK_UC_LOCK_DURATION"),
    ("r0263:u", "", "LOCK_CYCLES.CACHE_LOCK_DURATION"),
    ("r0279:u", "", "IDQ.EMPTY"),
    ("r0479:u", "", "IDQ.MITE_UOPS"),
    ("r0879:u", "", "IDQ.DSB_UOPS"),
    ("r1079:u", "", "IDQ.MS_DSB_UOPS"),
    ("r2079:u", "", "IDQ.MS_MITE_UOPS"),
    ("r3079:u", "", "IDQ.MS_UOPS"),
    ("r01001879:u", "", "IDQ.ALL_DSB_CYCLES_ANY_UOPS"),
    ("r04001879:u", "", "IDQ.ALL_DSB_CYCLES_4_UOPS"),
    ("r01002479:u", "", "IDQ.ALL_MITE_CYCLES_ANY_UOPS"),
    ("r04002479:u", "", "IDQ.ALL_MITE_CYCLES_4_UOPS"),
    ("r3c79:u", "", "IDQ.MITE_ALL_UOPS"),
    ("r0280:u", "", "ICACHE.MISSES"),
    ("r0185:u", "", "ITLB_MISSES.MISS_CAUSES_A_WALK"),
    ("r0285:u", "", "ITLB_MISSES.WALK_COMPLETED_4K"),
    ("r0485:u", "", "ITLB_MISSES.WALK_COMPLETED_2M_4M"),
    ("r0e85:u", "", "ITLB_MISSES.WALK_COMPLETED"),
    ("r1085:u", "", "ITLB_MISSES.WALK_DURATION"),
    ("r2085:u", "", "ITLB_MISSES.STLB_HIT_4K"),
    ("r4085:u", "", "ITLB_MISSES.STLB_HIT_2M"),
    ("r6085:u", "", "ITLB_MISSES.STLB_HIT"),
    ("r0187:u", "", "ILD_STALL.LCP"),
    ("r0487:u", "", "ILD_STALL.IQ_FULL"),
    ("r4188:u", "", "BR_INST_EXEC.COND.NOTAKEN"),
    ("r8188:u", "", "BR_INST_EXEC.COND.TAKEN"),
    ("r8288:u", "", "BR_INST_EXEC.DIRECT_JMP.TAKEN"),
    ("r8488:u", "", "BR_INST_EXEC.INDIRECT_JMP_NON_CALL_RET.TAKEN"),
    ("r8888:u", "", "BR_INST_EXEC.RETURN_NEAR.TAKEN"),
    ("r9088:u", "", "BR_INST_EXEC.DIRECT_NEAR_CALL.TAKEN"),
    ("ra088:u", "", "BR_INST_EXEC.INDIRECT_NEAR_CALL.TAKEN"),
    ("rff88:u", "", "BR_INST_EXEC.ALL_BRANCHES"),
    ("r4189:u", "", "BR_MISP_EXEC.COND.NOTAKEN"),
    ("r8189:u", "", "BR_MISP_EXEC.COND.TAKEN"),
    ("r8489:u", "", "BR_MISP_EXEC.INDIRECT_JMP_NON_CALL_RET.TAKEN"),
    ("r8889:u", "", "BR_MISP_EXEC.RETURN_NEAR.TAKEN"),
    ("r9089:u", "", "BR_MISP_EXEC.DIRECT_NEAR_CALL.TAKEN"),
    ("ra089:u", "", "BR_MISP_EXEC.INDIRECT_NEAR_CALL.TAKEN"),
    ("rff89:u", "", "BR_MISP_EXEC.ALL_BRANCHES"),
    ("r019c:u", "", "IDQ_UOPS_NOT_DELIVERED.CORE"),
    ("r01a1:u", "", "UOPS_EXECUTED_PORT.PORT_0"),
    ("r02a1:u", "", "UOPS_EXECUTED_PORT.PORT_1"),
    ("r04a1:u", "", "UOPS_EXECUTED_PORT.PORT_2"),
    ("r08a1:u", "", "UOPS_EXECUTED_PORT.PORT_3"),
    ("r10a1:u", "", "UOPS_EXECUTED_PORT.PORT_4"),
    ("r20a1:u", "", "UOPS_EXECUTED_PORT.PORT_5"),
    ("r40a1:u", "", "UOPS_EXECUTED_PORT.PORT_6"),
    ("r80a1:u", "", "UOPS_EXECUTED_PORT.PORT_7"),
    ("r01a2:u", "", "RESOURCE_STALLS.ANY"),
    ("r04a2:u", "", "RESOURCE_STALLS.RS"),
    ("r08a2:u", "", "RESOURCE_STALLS.SB"),
    ("r10a2:u", "", "RESOURCE_STALLS.ROB"),
    ("r020001a3:u", "", "CYCLE_ACTIVITY.CYCLES_L2_PENDING"),
    ("r020002a3:u", "", "CYCLE_ACTIVITY.CYCLES_LDM_PENDING"),
    ("r05a3:u",     "", "CYCLE_ACTIVITY.STALLS_L2_PENDING"),
    ("r080008a3:u", "", "CYCLE_ACTIVITY.CYCLES_L1D_PENDING"),
    ("r0c000ca3:u", "", "CYCLE_ACTIVITY.STALLS_L1D_PENDING"),
    ("r01a8:u", "", "LSD.UOPS"),
    ("r01ae:u", "", "ITLB.ITLB_FLUSH"),
    ("r01b0:u", "", "OFFCORE_REQUESTS.DEMAND_DATA_RD"),
    ("r02b0:u", "", "OFFCORE_REQUESTS.DEMAND_CODE_RD"),
    ("r04b0:u", "", "OFFCORE_REQUESTS.DEMAND_RFO"),
    ("r08b0:u", "", "OFFCORE_REQUESTS.ALL_DATA_RD"),
    ("r02b1:u", "", "UOPS_EXECUTED.CORE"),
    ("r11bc:u", "", "PAGE_WALKER_LOADS.DTLB_L1"),
    ("r21bc:u", "", "PAGE_WALKER_LOADS.ITLB_L1"),
    ("r12bc:u", "", "PAGE_WALKER_LOADS.DTLB_L2"),
    ("r22bc:u", "", "PAGE_WALKER_LOADS.ITLB_L2"),
    ("r14bc:u", "", "PAGE_WALKER_LOADS.DTLB_L3"),
    ("r24bc:u", "", "PAGE_WALKER_LOADS.ITLB_L3"),
    ("r18bc:u", "", "PAGE_WALKER_LOADS.DTLB_MEMORY"),
    ("r28bc:u", "", "PAGE_WALKER_LOADS.ITLB_MEMORY"),
    ("r01bd:u", "", "TLB_FLUSH.DTLB_THREAD"),
    ("r20bd:u", "", "TLB_FLUSH.STLB_ANY"),
    ("r00c0:u", "instructions:u", "INST_RETIRED.ANY_P"),
    ("r01c0:u", "", "INST_RETIRED.ALL"),
    ("r08c1:u", "", "OTHER_ASSISTS.AVX_TO_SSE"),
    ("r10c1:u", "", "OTHER_ASSISTS.SSE_TO_AVX"),
    ("r40c1:u", "", "OTHER_ASSISTS.ANY_WB_ASSIST"),
    ("r01c2:u", "", "UOPS_RETIRED.ALL"),
    ("r02c2:u", "", "UOPS_RETIRED.RETIRE_SLOTS"),
    ("r02c3:u", "", "MACHINE_CLEARS.MEMORY_ORDERING"),
    ("r04c3:u", "", "MACHINE_CLEARS.SMC"),
    ("r20c3:u", "", "MACHINE_CLEARS.MASKMOV"),
    ("r00c4:u", "branch-instructions:u", "BR_INST_RETIRED.ALL_BRANCHES"),
    ("r01c4:u", "", "BR_INST_RETIRED.CONDITIONAL"),
    ("r02c4:u", "", "BR_INST_RETIRED.NEAR_CALL"),
    ("r04c4:u", "", "BR_INST_RETIRED.ALL_BRANCHES"),
    ("r08c4:u", "", "BR_INST_RETIRED.NEAR_RETURN"),
    ("r10c4:u", "", "BR_INST_RETIRED.NOT_TAKEN"),
    ("r20c4:u", "", "BR_INST_RETIRED.NEAR_TAKEN"),
    ("r40c4:u", "", "BR_INST_RETIRED.FAR_BRANCH"),
    ("r00c5:u", "branch-misses:u", "BR_MISP_RETIRED.ALL_BRANCHES"),
    ("r01c5:u", "", "BR_MISP_RETIRED.CONDITIONAL"),
    ("r04c5:u", "", "BR_MISP_RETIRED.ALL_BRANCHES"),
    ("r20c5:u", "", "BR_MISP_RETIRED.NEAR_TAKEN"),
    ("r02ca:u", "", "FP_ASSIST.X87_OUTPUT"),
    ("r04ca:u", "", "FP_ASSIST.X87_INPUT"),
    ("r08ca:u", "", "FP_ASSIST.SIMD_OUTPUT"),
    ("r10ca:u", "", "FP_ASSIST.SIMD_INPUT"),
    ("r1eca:u", "", "FP_ASSIST.ANY"),
    ("r20cc:u", "", "ROB_MISC_EVENTS.LBR_INSERTS"),
    ("r11d0:u", "", "MEM_UOPS_RETIRED.STLB_MISS.LOADS"),
    ("r12d0:u", "", "MEM_UOPS_RETIRED.STLB_MISS.STORES"),
    ("r21d0:u", "", "MEM_UOPS_RETIRED.LOCK.LOADS"),
    ("r22d0:u", "", "MEM_UOPS_RETIRED.LOCK.STORES"),
    ("r41d0:u", "", "MEM_UOPS_RETIRED.SPLIT.LOADS"),
    ("r42d0:u", "", "MEM_UOPS_RETIRED.SPLIT.STORES"),
    ("r81d0:u", "", "MEM_UOPS_RETIRED.ALL.LOADS"),
    ("r82d0:u", "", "MEM_UOPS_RETIRED.ALL.STORES"),
    ("r01d1:u", "", "MEM_LOAD_UOPS_RETIRED.L1_HIT"),
    ("r02d1:u", "", "MEM_LOAD_UOPS_RETIRED.L2_HIT"),
    ("r04d1:u", "", "MEM_LOAD_UOPS_RETIRED.L3_HIT"),
    ("r08d1:u", "", "MEM_LOAD_UOPS_RETIRED.L1_MISS"),
    ("r10d1:u", "", "MEM_LOAD_UOPS_RETIRED.L2_MISS"),
    ("r20d1:u", "", "MEM_LOAD_UOPS_RETIRED.L3_MISS"),
    ("r40d1:u", "", "MEM_LOAD_UOPS_RETIRED.HIT_LFB"),
    ("r01d2:u", "", "MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_MISS"),
    ("r02d2:u", "", "MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_HIT"),
    ("r04d2:u", "", "MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_HITM"),
    ("r08d2:u", "", "MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_NONE"),
    ("r01d3:u", "", "MEM_LOAD_UOPS_L3_MISS_RETIRED.LOCAL_DRAM"),
    ("r1fe6:u", "", "BACLEARS.ANY"),
    ("r01f0:u", "", "L2_TRANS.DEMAND_DATA_RD"),
    ("r02f0:u", "", "L2_TRANS.RFO"),
    ("r04f0:u", "", "L2_TRANS.CODE_RD"),
    ("r08f0:u", "", "L2_TRANS.ALL_PF"),
    ("r10f0:u", "", "L2_TRANS.L1D_WB"),
    ("r20f0:u", "", "L2_TRANS.L2_FILL"),
    ("r40f0:u", "", "L2_TRANS.L2_WB"),
    ("r80f0:u", "", "L2_TRANS.ALL_REQUESTS"),
    ("r01f1:u", "", "L2_LINES_IN.I"),
    ("r02f1:u", "", "L2_LINES_IN.S"),
    ("r04f1:u", "", "L2_LINES_IN.E"),
    ("r07f1:u", "", "L2_LINES_IN.ALL"),
    ("r05f2:u", "", "L2_LINES_OUT.DEMAND_CLEAN"),
    ("r06f2:u", "", "L2_LINES_OUT.DEMAND_DIRTY")
]]

def parseargs():
    def perfctr(s):
        counter = filter(lambda (ctr): ctr.mnemonic == s.lower(), haswell)
        if not counter:
            raise argparse.ArgumentTypeError("Unrecognized performance counter " + s)
        return counter[0]

    def perfctrs(s):
        if s == "all":
            return haswell
        return list(set(map( perfctr, s.strip().lower().split(','))))

    cycles = [c for c in haswell if c.mnemonic == "cycles:u"][0]

    parser = argparse.ArgumentParser(prog="lperf", description='perf wrapper for varying execution contexts')
    parser.add_argument('-e', '--events', type=perfctrs, default="all", help="Comma separated list of event code or mnemonic, ex. cycles:u,r0107:u")
    parser.add_argument('-n', '--iterations', type=int, default=1)
    parser.add_argument('-r', '--repeat', type=int, default=1, help="Average results over multiple runs, using perf-stat -r")
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('--env-offset', type=int, default=0, help="Number of bytes initially added to environment")
    parser.add_argument('--env-increment', type=int, default=1, help="Number of characters added to environment each iteration")
    parser.add_argument('--enumerate', default=False, action='store_true', help="Iteration number as program argument")
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

            prfevnt = ','.join(map(lambda (c): c.mnemonic, current))
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
        row = [event.name, event.mnemonic] + data[event]['count']
        args.output.write(",".join(map(str, row)) + "\n")
