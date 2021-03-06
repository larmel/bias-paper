import subprocess

class Event:
    def __init__(self, event, umask, name, cmask = 0x00, alias = None, msr = 0xf):
        self.event = event
        self.umask = umask
        self.cmask = cmask
        self.alias = alias
        self.name = name
        self.msr = msr

    def mnemonic(self):
        return self.perfcode() if self.alias == None else "%s:u" % self.alias

    def perfcode(self):
        code = (self.cmask << 24) | (self.umask << 8) | self.event
        return ("r%04x:u" if self.cmask == 0x0 else "r%08x:u") % code

    def __hash__(self):
        return hash((self.event, self.umask, self.cmask))

    def __eq__(self, other):
        return (self.event, self.umask, self.cmask) == (other.event, other.umask, other.cmask)

# Try to determine the CPU we are running on
model_name = subprocess.check_output("grep 'model name' /proc/cpuinfo", shell=True)

haswell = []
core2 = []
registers = 0

# configuration based on detected architecture
if "Intel(R) Core(TM)2" in model_name:
    events = core2
    registers = 2
elif "Intel(R) Core(TM) i7-4" in model_name:
    events = haswell
    registers = 4

def sample(event_list):
    batch = []
    for e in event_list:
        if e.msr < 0xf:
            if len(batch) == 0:
                batch += [e]
                yield batch
            else: 
                yield batch
                batch = [e]
                yield batch
                batch = []
        else:
            batch += [e]
            if (len(batch) == registers):
                yield batch
                batch = []
    if len(batch) > 0:
        yield batch
    return

# See performance-counters.ods for full reference.
haswell += [
    Event(0x03, 0x02, name = "LD_BLOCKS.STORE_FORWARD"),
    Event(0x03, 0x08, name = "LD_BLOCKS.NO_SR"),
    Event(0x05, 0x01, name = "MISALIGN_MEM_REF.LOADS"),
    Event(0x05, 0x02, name = "MISALIGN_MEM_REF.STORES"),
    Event(0x07, 0x01, name = "LD_BLOCKS_PARTIAL.ADDRESS_ALIAS"),
    Event(0x08, 0x01, name = "DTLB_LOAD_MISSES.MISS_CAUSES_A_WALK"),
    Event(0x08, 0x02, name = "DTLB_LOAD_MISSES.WALK_COMPLETED_4K"),
    Event(0x08, 0x04, name = "DTLB_LOAD_MISSES.WALK_COMPLETED_2M_4M"),
    Event(0x08, 0x0e, name = "DTLB_LOAD_MISSES.WALK_COMPLETED"),
    Event(0x08, 0x10, name = "DTLB_LOAD_MISSES.WALK_DURATION"),
    Event(0x08, 0x20, name = "DTLB_LOAD_MISSES.STLB_HIT_4K"),
    Event(0x08, 0x40, name = "DTLB_LOAD_MISSES.STLB_HIT_2M"),
    Event(0x08, 0x60, name = "DTLB_LOAD_MISSES.STLB_HIT"),
    Event(0x08, 0x80, name = "DTLB_LOAD_MISSES.PDE_CACHE_MISS"),
    Event(0x0d, 0x03, name = "INT_MISC.RECOVERY_CYCLES"),
    Event(0x0e, 0x01, name = "UOPS_ISSUED.ANY"),
    Event(0x0e, 0x10, name = "UOPS_ISSUED.FLAGS_MERGE"),
    Event(0x0e, 0x20, name = "UOPS_ISSUED.SLOW_LEA"),
    Event(0x0e, 0x40, name = "UOPS_ISSUED.SiNGLE_MUL"),
    Event(0x24, 0x21, name = "L2_RQSTS.DEMAND_DATA_RD_MISS"),
    Event(0x24, 0x41, name = "L2_RQSTS.DEMAND_DATA_RD_HIT"),
    Event(0x24, 0xe1, name = "L2_RQSTS.ALL_DEMAND_DATA_RD"),
    Event(0x24, 0x42, name = "L2_RQSTS.RFO_HIT"),
    Event(0x24, 0x22, name = "L2_RQSTS.RFO_MISS"),
    Event(0x24, 0xe2, name = "L2_RQSTS.ALL_RFO"),
    Event(0x24, 0x44, name = "L2_RQSTS.CODE_RD_HIT"),
    Event(0x24, 0x24, name = "L2_RQSTS.CODE_RD_MISS"),
    Event(0x24, 0x27, name = "L2_RQSTS.ALL_DEMAND_MISS"),
    Event(0x24, 0xe7, name = "L2_RQSTS.ALL_DEMAND_REFERENCES"),
    Event(0x24, 0xe4, name = "L2_RQSTS.ALL_CODE_RD"),
    Event(0x24, 0x50, name = "L2_RQSTS.L2_PF_HIT"),
    Event(0x24, 0x30, name = "L2_RQSTS.L2_PF_MISS"),
    Event(0x24, 0xf8, name = "L2_RQSTS.ALL_PF"),
    Event(0x24, 0x3f, name = "L2_RQSTS.MISS"),
    Event(0x24, 0xff, name = "L2_RQSTS.REFERENCES"),
    Event(0x27, 0x50, name = "L2_DEMAND_RQSTS.WB_HIT"),
    Event(0x2e, 0x4f, name = "LONGEST_LAT_CACHE.REFERENCE", alias = "cache-references"),
    Event(0x2e, 0x41, name = "LONGEST_LAT_CACHE.MISS", alias = "cache-misses"),
    Event(0x3c, 0x00, name = "CPU_CLK_UNHALTED.THREAD_P", alias = "cycles"),
    Event(0x3c, 0x01, name = "CPU_CLK_THREAD_UNHALTED.REF_XCLK", alias = "bus-cycles"),
    Event(0x48, 0x01, name = "L1D_PEND_MISS.PENDING"),
    Event(0x49, 0x01, name = "DTLB_STORE_MISSES.MISS_CAUSES_A_WALK"),
    Event(0x49, 0x02, name = "DTLB_STORE_MISSES.WALK_COMPLETED_4K"),
    Event(0x49, 0x04, name = "DTLB_STORE_MISSES.WALK_COMPLETED_2M_4M"),
    Event(0x49, 0x0e, name = "DTLB_STORE_MISSES.WALK_COMPLETED"),
    Event(0x49, 0x10, name = "DTLB_STORE_MISSES.WALK_DURATION"),
    Event(0x49, 0x20, name = "DTLB_STORE_MISSES.STLB_HIT_4K"),
    Event(0x49, 0x40, name = "DTLB_STORE_MISSES.STLB_HIT_2M"),
    Event(0x49, 0x60, name = "DTLB_STORE_MISSES.STLB_HIT"),
    Event(0x49, 0x80, name = "DTLB_STORE_MISSES.PDE_CACHE_MISS"),
    Event(0x4c, 0x01, name = "LOAD_HIT_PRE.SW_PF"),
    Event(0x4c, 0x02, name = "LOAD_HIT_PRE.HW_PF"),
    Event(0x51, 0x01, name = "L1D.REPLACEMENT"),
    Event(0x58, 0x04, name = "MOVE_ELIMINATION.INT_NOT_ELIMINATED"),
    Event(0x58, 0x08, name = "MOVE_ELIMINATION.SIMD_NOT_ELIMINATED"),
    Event(0x58, 0x01, name = "MOVE_ELIMINATION.INT_ELIMINATED"),
    Event(0x58, 0x02, name = "MOVE_ELIMINATION.SIMD_ELIMINATED"),
    Event(0x5c, 0x01, name = "CPL_CYCLES.RING0"),
    Event(0x5c, 0x02, name = "CPL_CYCLES.RING123"),
    Event(0x5e, 0x01, name = "RS_EVENTS.EMPTY_CYCLES"),
    Event(0x60, 0x01, name = "OFFCORE_REQUESTS_OUTSTANDING.DEMAND_DATA_RD"),
    Event(0x60, 0x02, name = "OFFCORE_REQUESTS_OUTSTANDING.DEMAND_CODE_RD"),
    Event(0x60, 0x04, name = "OFFCORE_REQUESTS_OUTSTANDING.DEMAND_RFO"),
    Event(0x60, 0x08, name = "OFFCORE_REQUESTS_OUTSTANDING.ALL_DATA_RD"),
    Event(0x63, 0x01, name = "LOCK_CYCLES.SPLIT_LOCK_UC_LOCK_DURATION"),
    Event(0x63, 0x02, name = "LOCK_CYCLES.CACHE_LOCK_DURATION"),
    Event(0x79, 0x02, name = "IDQ.EMPTY"),
    Event(0x79, 0x04, name = "IDQ.MITE_UOPS"),
    Event(0x79, 0x08, name = "IDQ.DSB_UOPS"),
    Event(0x79, 0x10, name = "IDQ.MS_DSB_UOPS"),
    Event(0x79, 0x20, name = "IDQ.MS_MITE_UOPS"),
    Event(0x79, 0x30, name = "IDQ.MS_UOPS"),
    Event(0x79, 0x18, cmask = 0x01, name = "IDQ.ALL_DSB_CYCLES_ANY_UOPS"),
    Event(0x79, 0x18, cmask = 0x04, name = "IDQ.ALL_DSB_CYCLES_4_UOPS"),
    Event(0x79, 0x24, cmask = 0x01, name = "IDQ.ALL_MITE_CYCLES_ANY_UOPS"),
    Event(0x79, 0x24, cmask = 0x04, name = "IDQ.ALL_MITE_CYCLES_4_UOPS"),
    Event(0x79, 0x3c, name = "IDQ.MITE_ALL_UOPS"),
    Event(0x80, 0x02, name = "ICACHE.MISSES"),
    Event(0x85, 0x01, name = "ITLB_MISSES.MISS_CAUSES_A_WALK"),
    Event(0x85, 0x02, name = "ITLB_MISSES.WALK_COMPLETED_4K"),
    Event(0x85, 0x04, name = "ITLB_MISSES.WALK_COMPLETED_2M_4M"),
    Event(0x85, 0x0e, name = "ITLB_MISSES.WALK_COMPLETED"),
    Event(0x85, 0x10, name = "ITLB_MISSES.WALK_DURATION"),
    Event(0x85, 0x20, name = "ITLB_MISSES.STLB_HIT_4K"),
    Event(0x85, 0x40, name = "ITLB_MISSES.STLB_HIT_2M"),
    Event(0x85, 0x60, name = "ITLB_MISSES.STLB_HIT"),
    Event(0x87, 0x01, name = "ILD_STALL.LCP"),
    Event(0x87, 0x04, name = "ILD_STALL.IQ_FULL"),
    Event(0x88, 0x41, name = "BR_INST_EXEC.COND.NOTAKEN"),
    Event(0x88, 0x81, name = "BR_INST_EXEC.COND.TAKEN"),
    Event(0x88, 0x82, name = "BR_INST_EXEC.DIRECT_JMP.TAKEN"),
    Event(0x88, 0x84, name = "BR_INST_EXEC.INDIRECT_JMP_NON_CALL_RET.TAKEN"),
    Event(0x88, 0x88, name = "BR_INST_EXEC.RETURN_NEAR.TAKEN"),
    Event(0x88, 0x90, name = "BR_INST_EXEC.DIRECT_NEAR_CALL.TAKEN"),
    Event(0x88, 0xa0, name = "BR_INST_EXEC.INDIRECT_NEAR_CALL.TAKEN"),
    Event(0x88, 0xff, name = "BR_INST_EXEC.ALL_BRANCHES"),
    Event(0x89, 0x41, name = "BR_MISP_EXEC.COND.NOTAKEN"),
    Event(0x89, 0x81, name = "BR_MISP_EXEC.COND.TAKEN"),
    Event(0x89, 0x84, name = "BR_MISP_EXEC.INDIRECT_JMP_NON_CALL_RET.TAKEN"),
    Event(0x89, 0x88, name = "BR_MISP_EXEC.RETURN_NEAR.TAKEN"),
    Event(0x89, 0x90, name = "BR_MISP_EXEC.DIRECT_NEAR_CALL.TAKEN"),
    Event(0x89, 0xa0, name = "BR_MISP_EXEC.INDIRECT_NEAR_CALL.TAKEN"),
    Event(0x89, 0xff, name = "BR_MISP_EXEC.ALL_BRANCHES"),
    Event(0x9c, 0x01, name = "IDQ_UOPS_NOT_DELIVERED.CORE"),
    Event(0xa1, 0x01, name = "UOPS_EXECUTED_PORT.PORT_0"),
    Event(0xa1, 0x02, name = "UOPS_EXECUTED_PORT.PORT_1"),
    Event(0xa1, 0x04, name = "UOPS_EXECUTED_PORT.PORT_2"),
    Event(0xa1, 0x08, name = "UOPS_EXECUTED_PORT.PORT_3"),
    Event(0xa1, 0x10, name = "UOPS_EXECUTED_PORT.PORT_4"),
    Event(0xa1, 0x20, name = "UOPS_EXECUTED_PORT.PORT_5"),
    Event(0xa1, 0x40, name = "UOPS_EXECUTED_PORT.PORT_6"),
    Event(0xa1, 0x80, name = "UOPS_EXECUTED_PORT.PORT_7"),
    Event(0xa2, 0x01, name = "RESOURCE_STALLS.ANY"),
    Event(0xa2, 0x04, name = "RESOURCE_STALLS.RS"),
    Event(0xa2, 0x08, name = "RESOURCE_STALLS.SB"),
    Event(0xa2, 0x10, name = "RESOURCE_STALLS.ROB"),
    Event(0xa3, 0x01, cmask = 0x02, name = "CYCLE_ACTIVITY.CYCLES_L2_PENDING"),
    Event(0xa3, 0x02, cmask = 0x02, name = "CYCLE_ACTIVITY.CYCLES_LDM_PENDING"),
    Event(0xa3, 0x05, name = "CYCLE_ACTIVITY.STALLS_L2_PENDING"),
    Event(0xa3, 0x08, cmask = 0x08, name = "CYCLE_ACTIVITY.CYCLES_L1D_PENDING"),
    Event(0xa3, 0x0c, cmask = 0x0c, name = "CYCLE_ACTIVITY.STALLS_L1D_PENDING"),
    Event(0xa8, 0x01, name = "LSD.UOPS"),
    Event(0xae, 0x01, name = "ITLB.ITLB_FLUSH"),
    Event(0xb0, 0x01, name = "OFFCORE_REQUESTS.DEMAND_DATA_RD"),
    Event(0xb0, 0x02, name = "OFFCORE_REQUESTS.DEMAND_CODE_RD"),
    Event(0xb0, 0x04, name = "OFFCORE_REQUESTS.DEMAND_RFO"),
    Event(0xb0, 0x08, name = "OFFCORE_REQUESTS.ALL_DATA_RD"),
    Event(0xb1, 0x02, name = "UOPS_EXECUTED.CORE"),
    Event(0xbc, 0x11, name = "PAGE_WALKER_LOADS.DTLB_L1"),
    Event(0xbc, 0x21, name = "PAGE_WALKER_LOADS.ITLB_L1"),
    Event(0xbc, 0x12, name = "PAGE_WALKER_LOADS.DTLB_L2"),
    Event(0xbc, 0x22, name = "PAGE_WALKER_LOADS.ITLB_L2"),
    Event(0xbc, 0x14, name = "PAGE_WALKER_LOADS.DTLB_L3"),
    Event(0xbc, 0x24, name = "PAGE_WALKER_LOADS.ITLB_L3"),
    Event(0xbc, 0x18, name = "PAGE_WALKER_LOADS.DTLB_MEMORY"),
    Event(0xbc, 0x28, name = "PAGE_WALKER_LOADS.ITLB_MEMORY"),
    Event(0xbd, 0x01, name = "TLB_FLUSH.DTLB_THREAD"),
    Event(0xbd, 0x20, name = "TLB_FLUSH.STLB_ANY"),
    Event(0xc0, 0x00, name = "INST_RETIRED.ANY_P", alias = "instructions"),
    Event(0xc0, 0x01, name = "INST_RETIRED.ALL"),
    Event(0xc1, 0x08, name = "OTHER_ASSISTS.AVX_TO_SSE"),
    Event(0xc1, 0x10, name = "OTHER_ASSISTS.SSE_TO_AVX"),
    Event(0xc1, 0x40, name = "OTHER_ASSISTS.ANY_WB_ASSIST"),
    Event(0xc2, 0x01, name = "UOPS_RETIRED.ALL"),
    Event(0xc2, 0x02, name = "UOPS_RETIRED.RETIRE_SLOTS"),
    Event(0xc3, 0x02, name = "MACHINE_CLEARS.MEMORY_ORDERING"),
    Event(0xc3, 0x04, name = "MACHINE_CLEARS.SMC"),
    Event(0xc3, 0x20, name = "MACHINE_CLEARS.MASKMOV"),
    Event(0xc4, 0x00, name = "BR_INST_RETIRED.ALL_BRANCHES", alias = "branch-instructions"),
    Event(0xc4, 0x01, name = "BR_INST_RETIRED.CONDITIONAL"),
    Event(0xc4, 0x02, name = "BR_INST_RETIRED.NEAR_CALL"),
    Event(0xc4, 0x04, name = "BR_INST_RETIRED.ALL_BRANCHES"),
    Event(0xc4, 0x08, name = "BR_INST_RETIRED.NEAR_RETURN"),
    Event(0xc4, 0x10, name = "BR_INST_RETIRED.NOT_TAKEN"),
    Event(0xc4, 0x20, name = "BR_INST_RETIRED.NEAR_TAKEN"),
    Event(0xc4, 0x40, name = "BR_INST_RETIRED.FAR_BRANCH"),
    Event(0xc5, 0x00, name = "BR_MISP_RETIRED.ALL_BRANCHES", alias = "branch-misses"),
    Event(0xc5, 0x01, name = "BR_MISP_RETIRED.CONDITIONAL"),
    Event(0xc5, 0x04, name = "BR_MISP_RETIRED.ALL_BRANCHES"),
    Event(0xc5, 0x20, name = "BR_MISP_RETIRED.NEAR_TAKEN"),
    Event(0xca, 0x02, name = "FP_ASSIST.X87_OUTPUT"),
    Event(0xca, 0x04, name = "FP_ASSIST.X87_INPUT"),
    Event(0xca, 0x08, name = "FP_ASSIST.SIMD_OUTPUT"),
    Event(0xca, 0x10, name = "FP_ASSIST.SIMD_INPUT"),
    Event(0xca, 0x1e, name = "FP_ASSIST.ANY"),
    Event(0xcc, 0x20, name = "ROB_MISC_EVENTS.LBR_INSERTS"),
    Event(0xd0, 0x11, name = "MEM_UOPS_RETIRED.STLB_MISS.LOADS"),
    Event(0xd0, 0x12, name = "MEM_UOPS_RETIRED.STLB_MISS.STORES"),
    Event(0xd0, 0x21, name = "MEM_UOPS_RETIRED.LOCK.LOADS"),
    Event(0xd0, 0x22, name = "MEM_UOPS_RETIRED.LOCK.STORES"),
    Event(0xd0, 0x41, name = "MEM_UOPS_RETIRED.SPLIT.LOADS"),
    Event(0xd0, 0x42, name = "MEM_UOPS_RETIRED.SPLIT.STORES"),
    Event(0xd0, 0x81, name = "MEM_UOPS_RETIRED.ALL.LOADS"),
    Event(0xd0, 0x82, name = "MEM_UOPS_RETIRED.ALL.STORES"),
    Event(0xd1, 0x01, name = "MEM_LOAD_UOPS_RETIRED.L1_HIT"),
    Event(0xd1, 0x02, name = "MEM_LOAD_UOPS_RETIRED.L2_HIT"),
    Event(0xd1, 0x04, name = "MEM_LOAD_UOPS_RETIRED.L3_HIT"),
    Event(0xd1, 0x08, name = "MEM_LOAD_UOPS_RETIRED.L1_MISS"),
    Event(0xd1, 0x10, name = "MEM_LOAD_UOPS_RETIRED.L2_MISS"),
    Event(0xd1, 0x20, name = "MEM_LOAD_UOPS_RETIRED.L3_MISS"),
    Event(0xd1, 0x40, name = "MEM_LOAD_UOPS_RETIRED.HIT_LFB"),
    Event(0xd2, 0x01, name = "MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_MISS"),
    Event(0xd2, 0x02, name = "MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_HIT"),
    Event(0xd2, 0x04, name = "MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_HITM"),
    Event(0xd2, 0x08, name = "MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_NONE"),
    Event(0xd3, 0x01, name = "MEM_LOAD_UOPS_L3_MISS_RETIRED.LOCAL_DRAM"),
    Event(0xe6, 0x1f, name = "BACLEARS.ANY"),
    Event(0xf0, 0x01, name = "L2_TRANS.DEMAND_DATA_RD"),
    Event(0xf0, 0x02, name = "L2_TRANS.RFO"),
    Event(0xf0, 0x04, name = "L2_TRANS.CODE_RD"),
    Event(0xf0, 0x08, name = "L2_TRANS.ALL_PF"),
    Event(0xf0, 0x10, name = "L2_TRANS.L1D_WB"),
    Event(0xf0, 0x20, name = "L2_TRANS.L2_FILL"),
    Event(0xf0, 0x40, name = "L2_TRANS.L2_WB"),
    Event(0xf0, 0x80, name = "L2_TRANS.ALL_REQUESTS"),
    Event(0xf1, 0x01, name = "L2_LINES_IN.I"),
    Event(0xf1, 0x02, name = "L2_LINES_IN.S"),
    Event(0xf1, 0x04, name = "L2_LINES_IN.E"),
    Event(0xf1, 0x07, name = "L2_LINES_IN.ALL"),
    Event(0xf2, 0x05, name = "L2_LINES_OUT.DEMAND_CLEAN"),
    Event(0xf2, 0x06, name = "L2_LINES_OUT.DEMAND_DIRTY")
]

core2 += [
    Event(0x03, 0x02, name = "LOAD_BLOCK.STA"),
    Event(0x03, 0x04, name = "LOAD_BLOCK.STD"),
    Event(0x03, 0x08, name = "LOAD_BLOCK.OVERLAP_STORE"),
    Event(0x03, 0x10, name = "LOAD_BLOCK.UNTIL_RETIRE"),
    Event(0x03, 0x20, name = "LOAD_BLOCK.L1D"),
    Event(0x04, 0x01, name = "SB_DRAIN_CYCLES"),
    Event(0x04, 0x02, name = "STORE_BLOCK.ORDER"),
    Event(0x04, 0x08, name = "STORE_BLOCK.SNOOP"),
    Event(0x06, 0x00, name = "SEGMENT_REG_LOADS"),
    Event(0x07, 0x00, name = "SSE_PRE_EXEC.NTA"),
    Event(0x07, 0x01, name = "SSE_PRE_EXEC.L1"),
    Event(0x07, 0x02, name = "SSE_PRE_EXEC.L2"),
    Event(0x07, 0x03, name = "SSE_PRE_EXEC.STORES"),
    Event(0x08, 0x01, name = "DTLB_MISSES.ANY"),
    Event(0x08, 0x02, name = "DTLB_MISSES.MISS_LD"),
    Event(0x08, 0x04, name = "DTLB_MISSES.L0_MISS_LD"),
    Event(0x08, 0x08, name = "DTLB_MISSES.MISS_ST"),
    Event(0x09, 0x01, name = "MEMORY_DISAMBIGUATION.RESET"),
    Event(0x09, 0x02, name = "MEMORY_DISAMBIGUATION.SUCCESS"),
    Event(0x0C, 0x01, name = "PAGE_WALKS.COUNT"),
    Event(0x0C, 0x02, name = "PAGE_WALKS.CYCLES"),
    Event(0x10, 0x00, name = "FP_COMP_OPS_EXE", msr = 0x1),
    Event(0x11, 0x00, name = "FP_ASSIST", msr = 0x2),
    Event(0x12, 0x00, name = "MUL", msr = 0x2),
    Event(0x13, 0x00, name = "DIV", msr = 0x2),
    Event(0x14, 0x00, name = "CYCLES_DIV_BUSY", msr = 0x1),
    Event(0x18, 0x00, name = "IDLE_DURING_DIV", msr = 0x1),
    Event(0x19, 0x00, name = "DELAYED_BYPASS.FP", msr = 0x2),
    Event(0x19, 0x01, name = "DELAYED_BYPASS.SIMD", msr = 0x2),
    Event(0x19, 0x02, name = "DELAYED_BYPASS.LOAD", msr = 0x2),
    Event(0x21, 0x40, name = "L2_ADS.CORE"),
    Event(0x23, 0x40, name = "L2_DBUS_BUSY_RD.CORE"),
    Event(0x24, 0x40, name = "L2_LINES_IN.CORE"),
    Event(0x24, 0x50, name = "L2_LINES_IN.CORE.PREFETCH"),
    Event(0x25, 0x40, name = "L2_M_LINES_IN.CORE"),
    Event(0x26, 0x40, name = "L2_LINES_OUT.CORE"),
    Event(0x26, 0x50, name = "L2_LINES_OUT.CORE.PREFETCH"),
    Event(0x27, 0x40, name = "L2_M_LINES_OUT.CORE"),
    Event(0x27, 0x50, name = "L2_M_LINES_OUT.CORE.PREFETCH"),
    Event(0x28, 0x4F, name = "L2_IFETCH.CORE.ALL"),
    Event(0x29, 0x4F, name = "L2_LD.CORE.ALL"),
    Event(0x29, 0x5F, name = "L2_LD.CORE.PREFETCH.ALL"),
    Event(0x2A, 0x4F, name = "L2_ST.CORE.ALL"),
    Event(0x2B, 0x4F, name = "L2_LOCK.CORE.ALL"),
    Event(0x2E, 0x4F, name = "L2_RQSTS.CORE.ALL"),
    Event(0x2E, 0x5F, name = "L2_RQSTS.CORE.PREFETCH.ALL"),
    Event(0x2E, 0x41, name = "L2_RQSTS.SELF.DEMAND.I_STATE"),
    Event(0x2E, 0x4F, name = "L2_RQSTS.SELF.DEMAND.MESI"),
    Event(0x30, 0x4F, name = "L2_REJECT_BUSQ.CORE.ALL"),
    Event(0x30, 0x5F, name = "L2_REJECT_BUSQ.CORE.PREFETCH.ALL"),
    Event(0x32, 0x40, name = "L2_NO_REQ.CORE"),
    Event(0x3A, 0x00, name = "EIST_TRANS"),
    Event(0x3B, 0xC0, name = "THERMAL_TRIP"),
    Event(0x3C, 0x00, name = "CPU_CLK_UNHALTED.CORE_P", alias = "cycles"),
    Event(0x3C, 0x01, name = "CPU_CLK_UNHALTED.BUS"),
    Event(0x3C, 0x02, name = "CPU_CLK_UNHALTED.NO_OTHER"),
    Event(0x40, 0x0F, name = "L1D_CACHE_LD.ALL"),
    Event(0x41, 0x0F, name = "L1D_CACHE_ST.ALL"),
    Event(0x42, 0x0F, name = "L1D_CACHE_LOCK.ALL"),
    Event(0x42, 0x10, name = "L1D_CACHE_LOCK_DURATION"),
    Event(0x43, 0x01, name = "L1D_ALL_REF"),
    Event(0x43, 0x02, name = "L1D_ALL_CACHE_REF"),
    Event(0x45, 0x0F, name = "L1D_REPL"),
    Event(0x46, 0x00, name = "L1D_M_REPL"),
    Event(0x47, 0x00, name = "L1D_M_EVICT"),
    Event(0x48, 0x00, name = "L1D_PEND_MISS"),
    Event(0x49, 0x01, name = "L1D_SPLIT.LOADS"),
    Event(0x49, 0x02, name = "L1D_SPLIT.STORES"),
    Event(0x4B, 0x00, name = "SSE_PRE_MISS.NTA"),
    Event(0x4B, 0x01, name = "SSE_PRE_MISS.L1"),
    Event(0x4B, 0x02, name = "SSE_PRE_MISS.L2"),
    Event(0x4C, 0x00, name = "LOAD_HIT_PRE"),
    Event(0x4E, 0x10, name = "L1D_PREFETCH.REQUESTS"),
    Event(0x80, 0x00, name = "L1I_READS"),
    Event(0x81, 0x00, name = "L1I_MISSES"),
    Event(0x82, 0x02, name = "ITLB.SMALL_MISS"),
    Event(0x82, 0x10, name = "ITLB.LARGE_MISS"),
    Event(0x82, 0x40, name = "ITLB.FLUSH"),
    Event(0x82, 0x12, name = "ITLB.MISSES"),
    Event(0x83, 0x02, name = "INST_QUEUE.FULL"),
    Event(0x86, 0x00, name = "CYCLES_L1I_MEM_STALLED"),
    Event(0x87, 0x00, name = "ILD_STALL"),
    Event(0x88, 0x00, name = "BR_INST_EXEC"),
    Event(0x89, 0x00, name = "BR_MISSP_EXEC"),
    Event(0x8A, 0x00, name = "BR_BAC_MISSP_EXEC"),
    Event(0x8B, 0x00, name = "BR_CND_EXEC"),
    Event(0x8C, 0x00, name = "BR_CND_MISSP_EXEC"),
    Event(0x8D, 0x00, name = "BR_IND_EXEC"),
    Event(0x8E, 0x00, name = "BR_IND_MISSP_EXEC"),
    Event(0x8F, 0x00, name = "BR_RET_EXEC"),
    Event(0x90, 0x00, name = "BR_RET_MISSP_EXEC"),
    Event(0x91, 0x00, name = "BR_RET_BAC_MISSP_EXEC"),
    Event(0x92, 0x00, name = "BR_CALL_EXEC"),
    Event(0x93, 0x00, name = "BR_CALL_MISSP_EXEC"),
    Event(0x94, 0x00, name = "BR_IND_CALL_EXEC"),
    Event(0x97, 0x00, name = "BR_TKN_BUBBLE_1"),
    Event(0x98, 0x00, name = "BR_TKN_BUBBLE_2"),
    Event(0xA0, 0x00, name = "RS_UOPS_DISPATCHED"),
    Event(0xA1, 0x01, name = "RS_UOPS_DISPATCHED.PORT0", msr = 0x1),
    Event(0xA1, 0x02, name = "RS_UOPS_DISPATCHED.PORT1", msr = 0x1),
    Event(0xA1, 0x04, name = "RS_UOPS_DISPATCHED.PORT2", msr = 0x1),
    Event(0xA1, 0x08, name = "RS_UOPS_DISPATCHED.PORT3", msr = 0x1),
    Event(0xA1, 0x10, name = "RS_UOPS_DISPATCHED.PORT4", msr = 0x1),
    Event(0xA1, 0x20, name = "RS_UOPS_DISPATCHED.PORT5", msr = 0x1),
    Event(0xAA, 0x01, name = "MACRO_INSTS.DECODED"),
    Event(0xAA, 0x08, name = "MACRO_INSTS.CISC_DECODED"),
    Event(0xAB, 0x01, name = "ESP.SYNCH"),
    Event(0xAB, 0x02, name = "ESP.ADDITIONS"),
    Event(0xB0, 0x00, name = "SIMD_UOPS_EXEC"),
    Event(0xB1, 0x00, name = "SIMD_SAT_UOP_EXEC"),
    Event(0xB3, 0x01, name = "SIMD_UOP_TYPE_EXEC.MUL"),
    Event(0xB3, 0x02, name = "SIMD_UOP_TYPE_EXEC.SHIFT"),
    Event(0xB3, 0x04, name = "SIMD_UOP_TYPE_EXEC.PACK"),
    Event(0xB3, 0x08, name = "SIMD_UOP_TYPE_EXEC.UNPACK"),
    Event(0xB3, 0x10, name = "SIMD_UOP_TYPE_EXEC.LOGICAL"),
    Event(0xB3, 0x20, name = "SIMD_UOP_TYPE_EXEC.ARITHMETIC"),
    Event(0xC0, 0x00, name = "INST_RETIRED.ANY_P"),
    Event(0xC0, 0x01, name = "INST_RETIRED.LOADS"),
    Event(0xC0, 0x02, name = "INST_RETIRED.STORES"),
    Event(0xC0, 0x04, name = "INST_RETIRED.OTHER"),
    Event(0xC1, 0x01, name = "X87_OPS_RETIRED.FXCH"),
    Event(0xC1, 0xFE, name = "X87_OPS_RETIRED.ANY"),
    Event(0xC2, 0x01, name = "UOPS_RETIRED.LD_IND_BR"),
    Event(0xC2, 0x02, name = "UOPS_RETIRED.STD_STA"),
    Event(0xC2, 0x04, name = "UOPS_RETIRED.MACRO_FUSION"),
    Event(0xC2, 0x07, name = "UOPS_RETIRED.FUSED"),
    Event(0xC2, 0x08, name = "UOPS_RETIRED.NON_FUSED"),
    Event(0xC2, 0x0F, name = "UOPS_RETIRED.ANY"),
    Event(0xC3, 0x01, name = "MACHINE_NUKES.SMC"),
    Event(0xC3, 0x04, name = "MACHINE_NUKES.MEM_ORDER"),
    Event(0xC4, 0x00, name = "BR_INST_RETIRED.ANY"),
    Event(0xC4, 0x01, name = "BR_INST_RETIRED.PRED_NOT_TAKEN"),
    Event(0xC4, 0x02, name = "BR_INST_RETIRED.MISPRED_NOT_TAKEN"),
    Event(0xC4, 0x04, name = "BR_INST_RETIRED.PRED_TAKEN"),
    Event(0xC4, 0x08, name = "BR_INST_RETIRED.MISPRED_TAKEN"),
    Event(0xC4, 0x0C, name = "BR_INST_RETIRED.TAKEN"),
    Event(0xC5, 0x00, name = "BR_INST_RETIRED.MISPRED"),
    Event(0xC6, 0x01, name = "CYCLES_INT_MASKED"),
    Event(0xC6, 0x02, name = "CYCLES_INT_PENDING_AND_MASKED"),
    Event(0xC7, 0x01, name = "SIMD_INST_RETIRED.PACKED_SINGLE"),
    Event(0xC7, 0x02, name = "SIMD_INST_RETIRED.SCALAR_SINGLE"),
    Event(0xC7, 0x04, name = "SIMD_INST_RETIRED.PACKED_DOUBLE"),
    Event(0xC7, 0x08, name = "SIMD_INST_RETIRED.SCALAR_DOUBLE"),
    Event(0xC7, 0x10, name = "SIMD_INST_RETIRED.VECTOR"),
    Event(0xC7, 0x1F, name = "SIMD_INST_RETIRED.ANY"),
    Event(0xC8, 0x00, name = "HW_INT_RCV"),
    Event(0xC9, 0x00, name = "ITLB_MISS_RETIRED"),
    Event(0xCA, 0x01, name = "SIMD_COMP_INST_RETIRED.PACKED_SINGLE"),
    Event(0xCA, 0x02, name = "SIMD_COMP_INST_RETIRED.SCALAR_SINGLE"),
    Event(0xCA, 0x04, name = "SIMD_COMP_INST_RETIRED.PACKED_DOUBLE"),
    Event(0xCA, 0x08, name = "SIMD_COMP_INST_RETIRED.SCALAR_DOUBLE"),
    Event(0xCB, 0x01, name = "MEM_LOAD_RETIRED.L1D_MISS", msr = 0x1),
    Event(0xCB, 0x02, name = "MEM_LOAD_RETIRED.L1D_LINE_MISS", msr = 0x1),
    Event(0xCB, 0x04, name = "MEM_LOAD_RETIRED.L2_MISS", msr = 0x1),
    Event(0xCB, 0x08, name = "MEM_LOAD_RETIRED.L2_LINE_MISS", msr = 0x1),
    Event(0xCB, 0x10, name = "MEM_LOAD_RETIRED.DTLB_MISS", msr = 0x1),
    Event(0xCC, 0x01, name = "FP_MMX_TRANS_TO_MMX"),
    Event(0xCC, 0x02, name = "FP_MMX_TRANS_TO_FP"),
    Event(0xCD, 0x00, name = "SIMD_ASSIST"),
    Event(0xCE, 0x00, name = "SIMD_INSTR_RETIRED"),
    Event(0xCF, 0x00, name = "SIMD_SAT_INSTR_RETIRED"),
    Event(0xD2, 0x01, name = "RAT_STALLS.ROB_READ_PORT"),
    Event(0xD2, 0x02, name = "RAT_STALLS.PARTIAL_CYCLES"),
    Event(0xD2, 0x04, name = "RAT_STALLS.FLAGS"),
    Event(0xD2, 0x08, name = "RAT_STALLS.FPSW"),
    Event(0xD2, 0x0F, name = "RAT_STALLS.ANY"),
    Event(0xD4, 0x01, name = "SEG_RENAME_STALLS.ES"),
    Event(0xD4, 0x02, name = "SEG_RENAME_STALLS.DS"),
    Event(0xD4, 0x04, name = "SEG_RENAME_STALLS.FS"),
    Event(0xD4, 0x08, name = "SEG_RENAME_STALLS.GS"),
    Event(0xD4, 0x0F, name = "SEG_RENAME_STALLS.ANY"),
    Event(0xD5, 0x01, name = "SEG_REG_RENAMES.ES"),
    Event(0xD5, 0x02, name = "SEG_REG_RENAMES.DS"),
    Event(0xD5, 0x04, name = "SEG_REG_RENAMES.FS"),
    Event(0xD5, 0x08, name = "SEG_REG_RENAMES.GS"),
    Event(0xD5, 0x0F, name = "SEG_REG_RENAMES.ANY"),
    Event(0xDC, 0x01, name = "RESOURCE_STALLS.ROB_FULL"),
    Event(0xDC, 0x02, name = "RESOURCE_STALLS.RS_FULL"),
    Event(0xDC, 0x04, name = "RESOURCE_STALLS.LD_ST"),
    Event(0xDC, 0x08, name = "RESOURCE_STALLS.FPCW"),
    Event(0xDC, 0x10, name = "RESOURCE_STALLS.BR_MISS_CLEAR"),
    Event(0xDC, 0x1F, name = "RESOURCE_STALLS.ANY"),
    Event(0xE0, 0x00, name = "BR_INST_DECODED"),
    Event(0xE4, 0x00, name = "BOGUS_BR"),
    Event(0xE6, 0x00, name = "BACLEARS"),
    Event(0xF0, 0x00, name = "PREF_RQSTS_UP"),
    Event(0xF8, 0x00, name = "PREF_RQSTS_DN")
]
