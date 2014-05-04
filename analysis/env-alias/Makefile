LPERF := ../../util/lperf

.PHONY: disable-aslr data

bin/loop: loop.c
	cc $+ -o $@

bin/analysis: alias-analysis.s
	cc $+ -o $@

disable-aslr:
	sudo bash -c "echo 0 > /proc/sys/kernel/randomize_va_space"


# This is the main result, which is used to plot the big graph. Already know
# that alias and resource stalls are interesting, so include those. The script
# is fastest with up to four counters, so keep it at max that size. Only
# the cycle count is actually plotted.
bin/two-4k-cycles.csv: disable-aslr bin/loop
	util/lperf -e cycles:u,r0107:u,r01a2:u,r02a3:u -n 512 -r 100 --env-increment 16 bin/loop > $@

# Same measurements as above, but with ALL counters. Reduce average to 10 to
# use a bit less time.
bin/two-4k-all.csv: disable-aslr bin/loop
	util/lperf -e all -n 512 -r 100 --env-increment 16 bin/loop > $@

# From these results, it should be apparant that two environments have alias.
# These are our values, but this might vary on other machines. These are the
# mod 16 = 0 values, but byte offsets around this that keeps stack alignment
# the same (from default 16 byte alignment) will also alias.
# Sanity check: offset2 = offset1 + 4196
SPIKE_OFFSET_1 := 3192
SPIKE_OFFSET_2 := 7288

# Now use these offsets to check what addresses g and inc has, using the
# instrumented assembly for printing stack addresses.
stack-addresses: disable-aslr bin/analysis
	$(LPERF) -e r0107:u --env-offset $(SPIKE_OFFSET_1) bin/analysis
	$(LPERF) -e r0107:u --env-offset $(SPIKE_OFFSET_2) bin/analysis

# These should alias with static data
static-addresses: bin/loop
	readelf -s $+ | grep -E ' i| j| k'

# To pinpoint what actually causes spike in cycle count, analyse a smaller area
# around one of the spikes. Use byte increment for environment instead to get
# more samples with bad performance (effectively sample the same context).
# Use the first spike, but if that happens to lie close to 0 this simple offset
# calculation fails.
# Sample 100 environments, starting with byte offset -50 from the first spike.
bin/spike-analysis-all.csv: disable-aslr bin/loop
	$(eval start := $(shell echo ${SPIKE_OFFSET_1}-50 | bc))
	$(LPERF) -e all -n 100 -r 100 --env-offset $(start) --env-increment 1 bin/loop > $@
