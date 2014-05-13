lperf := ../../util/lperf.py
median := ../../util/median.py
select := ../../util/select.py

.PHONY: all disable-aslr results
all: results

bin:
	mkdir -p bin

disable-aslr:
	sudo bash -c "echo 0 > /proc/sys/kernel/randomize_va_space"

# The instrumented assembly depends on the output of gcc -S. It has to be 
# crafted by hand, thus the assembly file is the dependency.
# The _length_ of the binary name has to be the same to not affect arguments.

bin/loop: loop.c | bin
	cc $< -o $@

bin/looq: alias-analysis.s | bin
	cc $< -o $@

bin/fixd: recursion-fix.c | bin
	cc $< -o $@ 

# This is the basis of all the analysis. Measure ALL counters over two 4K
# periods. From that we do median value and filtering to produce backing files
# needed for the article.
# Run the same test for instrumented binary to verify there are no observer
# effects.
# And again for the proposed fix, dynamically detecting alias condition and
# branching to an alternative execution path. 

bin/loop.csv: bin/loop | disable-aslr
	$(lperf) -e all -n 512 -r 10 --env-increment 16 $< > $@

bin/instrumented.csv: bin/looq | disable-aslr
	$(lperf) -e all -n 512 -r 10 --env-increment 16 $< > $@ 2> /dev/null 

bin/fixed.csv: bin/fixd | disable-aslr
	$(lperf) -e all -n 512 -r 10 --env-increment 16 $< > $@

# From these results, it should be apparant that two environments have alias.
# These are our values, but this might vary on other machines. These represent
# a point within a 16 byte alignment, so but byte offsets around this that 
# keeps stack alignment the same (because of default 16 byte alignment) will 
# also alias.
# Sanity check: offset2*16 = offset1*16 + 4196
spike_offset_1 := 200 # -> 3200 bytes
spike_offset_2 := 456 # -> 7296 bytes

# Compare median values with the two spikes. Add 3 to skip through name, mnemonic
# and offset 0 of the result file.
bin/comparison.csv: bin/loop.csv
	$(median) --input $< > c.tmp
	$(eval a := $(shell echo ${spike_offset_1}+3 | bc))
	$(eval b := $(shell echo ${spike_offset_2}+3 | bc))
	cut -d ',' -f $(a) $< > a.tmp
	cut -d ',' -f $(b) $< > b.tmp
	paste -d ',' c.tmp a.tmp b.tmp > $@
	rm a.tmp b.tmp c.tmp

# Filter out only cycle count for plotting the whole 8k range
bin/cycles.csv: bin/loop.csv
	cat $< | $(select) -e cycles:u > $@

# Make a new set of results needed for the paper. Aliasing offsets are hard-
# coded here, and needs to be controlled manually. Should see aliasing 
# addresses from static/automatic output if set correctly.
results: bin/loop.csv bin/instrumented.csv bin/fixed.csv bin/comparison.csv bin/cycles.csv
	@echo ""
	@echo "==== Static variables ==========="
	readelf -s bin/loop | grep -E ' i| j| k'
	@echo ""
	@echo "==== Automatic variables ========"
	$(eval a := $(shell echo ${spike_offset_1}*16 | bc)) # x16 to get bytes
	$(eval b := $(shell echo ${spike_offset_2}*16 | bc))
	$(lperf) -e r0107:u --env-offset $(a) bin/looq
	$(lperf) -e r0107:u --env-offset $(b) bin/looq
	@echo ""
	# If you are satisfied, mv bin/*.csv results
