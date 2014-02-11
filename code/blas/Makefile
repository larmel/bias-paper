SHELL := /bin/bash
LPERF := ../../util/lperf

# Specify what to provide linker, as -l$(BLAS). Use 'blas' for
# default implementation, or 'atlas' that is installed.
BLAS := blas

.DEFAULT: bin/gemv
.PHONY: benchmark

disable-aslr:
	@echo "Disabling address randomization ..."
	sudo bash -c "echo 0 > /proc/sys/kernel/randomize_va_space"

bin/gemv: gemv.c
	gcc -std=c99 $< -o $@ -l$(BLAS)

# Do three invocations of lperf to measure performance for different memory
# addresses. Some tape and glue in bash to gather the results in a csv file
# `benchmark.csv` at the end.
# Case (a), (b), (c) with 1 iteration
# Case (a), (b), (c) with 100 iterations
# Separate counter names and mnemonics from first and second column.
# The order is preserved, so these columns are identical in each result.
benchmark: bin/gemv disable-aslr
	$(LPERF) -e cycles:u,r0107:u -n 1 $< 0 0 1  > lperf.a.1.csv 2> output.a.1.out 
	$(LPERF) -e cycles:u,r0107:u -n 1 $< 1024 0 1 > lperf.b.1.csv 2> output.b.1.out 
	$(LPERF) -e cycles:u,r0107:u -n 1 $< 2048 0 1 > lperf.c.1.csv 2> output.c.1.out

	$(LPERF) -e cycles:u,r0107:u -n 1 $< 0 0 100  > lperf.a.100.csv 2> output.a.100.out 
	$(LPERF) -e cycles:u,r0107:u -n 1 $< 1024 0 100 > lperf.b.100.csv 2> output.b.100.out 
	$(LPERF) -e cycles:u,r0107:u -n 1 $< 2048 0 100 > lperf.c.100.csv 2> output.c.100.out

	@cut -d ',' -f 1 lperf.a.1.csv > counters.tmp
	@cut -d ',' -f 2 lperf.a.1.csv > mnemonic.tmp

	@cut -d ',' -f 4 lperf.a.1.csv > a.1.tmp
	@cut -d ',' -f 4 lperf.b.1.csv > b.1.tmp
	@cut -d ',' -f 4 lperf.c.1.csv > c.1.tmp

	@cut -d ',' -f 4 lperf.a.100.csv > a.100.tmp
	@cut -d ',' -f 4 lperf.b.100.csv > b.100.tmp
	@cut -d ',' -f 4 lperf.c.100.csv > c.100.tmp

	@paste -d ',' counters.tmp mnemonic.tmp a.1.tmp b.1.tmp c.1.tmp /dev/null a.100.tmp b.100.tmp c.100.tmp > benchmark.csv
	@rm *.tmp
	mv *.csv *.out bin



