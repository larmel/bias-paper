lperf := ../../util/lperf.py
median := ../../util/median.py
select := ../../util/select.py

disable-aslr:
	sudo bash -c "echo 0 > /proc/sys/kernel/randomize_va_space"

.PHONY: disable-aslr static-addresses


bin/loop: loop.c
	cc $< -o $@

loop.s: loop.c
	cc $< -S -o $@

# This is the basis of all the analysis. Measure ALL counters over two 4K
# periods. From that we do median value and filtering to produce backing files
# needed for the article
bin/loop.csv: bin/loop disable-aslr
	$(lperf) -e all -n 512 -r 10 --env-increment 16 $< > $@


# From these results, it should be apparant that two environments have alias.
# These are our values, but this might vary on other machines. These are the
# mod 16 values, but byte offsets around this that keeps stack alignment
# the same (from default 16 byte alignment) will also alias.
# Sanity check: offset2*16 = offset1*16 + 4196
spike_offset_1 := 200 # -> 3200 bytes
spike_offset_2 := 456 # -> 7296 bytes


# Compare median values with the two spikes. Add 3 to skip through name, mnemonic
# and offset 0 of the result file.
bin/comparison.csv: 
	$(median) --input bin/loop.csv > c.tmp
	$(eval a := $(shell echo ${spike_offset_1}+3 | bc))
	$(eval b := $(shell echo ${spike_offset_2}+3 | bc))
	cut -d ',' -f $(a) bin/loop.csv > a.tmp
	cut -d ',' -f $(b) bin/loop.csv > b.tmp
	paste -d ',' c.tmp a.tmp b.tmp > $@
	rm a.tmp b.tmp c.tmp

# Filter out only cycle count for plotting the whole 8k range
bin/cycles.csv: 
	cat bin/loop.csv | $(select) -e cycles:u > $@


# The analysis assembly depends on the output of gcc -S. It has to be 
# crafted by hand, thus the assembly file is the dependency.
# Todo: update with newest compiler output if necessary
# Nb: The length of the name has to be the same -- first argument.
bin/looq: alias-analysis.s
	cc $+ -o $@

# Now use these offsets to check what addresses g and inc has, using the
# instrumented assembly for printing stack addresses. Multiply by 16 to get
# offsets in bytes.
# This will print to terminal, so have to copy paste manually.
stack-addresses: bin/looq disable-aslr 
	$(eval a := $(shell echo ${spike_offset_1}*16 | bc))
	$(eval b := $(shell echo ${spike_offset_2}*16 | bc))
	$(lperf) -e r0107:u --env-offset $(a) $<
	$(lperf) -e r0107:u --env-offset $(b) $<

# These should alias with static data
static-addresses: bin/loop
	readelf -s $< | grep -E ' i| j| k'










# Deprecated below -------

# This is the main result, which is used to plot the big graph. Already know
# that alias and resource stalls are interesting, so include those. The script
# is fastest with up to four counters, so keep it at max that size. Only
# the cycle count is actually plotted.
bin/two-4k-cycles.csv: disable-aslr bin/loop
	util/lperf -e cycles:u,r0107:u,r01a2:u,r02a3:u -n 512 -r 100 --env-increment 16 bin/loop > $@

# To pinpoint what actually causes spike in cycle count, analyse a smaller area
# around one of the spikes. Use byte increment for environment instead to get
# more samples with bad performance (effectively sample the same context).
# Use the first spike, but if that happens to lie close to 0 this simple offset
# calculation fails.
# Sample 100 environments, starting with byte offset -50 from the first spike.
bin/spike-analysis-all.csv: disable-aslr bin/loop
	$(eval start := $(shell echo ${spike_offset_1}-50 | bc))
	$(lperf) -e all -n 100 -r 100 --env-offset $(start) --env-increment 1 bin/loop > $@


# Take 2 on this, just analyse best case/worst case in two samples. More 
# interesting to have real numbers backing the table. Presenting 0.999
# correlation has little value. Easily reproduce table by only having the
# highest correlating counters here.
bin/spike.csv: disable-aslr bin/loop
	$(eval start := $(shell echo ${spike_offset_1}-16 | bc))
	$(eval counters := cycles:u,bus-cycles:u,r0107:u,r02a3:u,r01a2:u,r025c:u,r04a1:u,r05a3:u,r2224:u,r04b0:u,re224:u,r0460:u,r02f0:u,r2049:u,r40f0:u,re124:u,r10d1:u,r4224:u,r01a8:u,r08a1:u,r80a1:u,r10a1:u,r40a1:u,r01a1:u,r02a1:u,r20a1:u,r04a2:u)
	$(lperf) -e $(counters) -n 2 -r 100 --env-offset $(start) --env-increment 16 bin/loop > $@
