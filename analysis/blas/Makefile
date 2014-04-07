SHELL := /bin/bash
LPERF := ../../util/lperf

PERFCOUNTERS := all
REPEAT := 4

.PHONY: benchmark atlas default heatmap


atlas:
	gcc -std=c99 gemv.c -o bin/gemv -I/usr/local/atlas/include -L/usr/local/atlas/lib -lsatlas

default:
	gcc -std=c99 gemv.c -o bin/gemv -lblas

bin/gemv: gemv.c
	gcc -std=c99 $< -o $@ -I/usr/local/atlas/include -L/usr/local/atlas/lib -lsatlas
	#gcc -std=c99 $< -o $@ -lblas
	#gcc -std=c99 $< -o $@ -L~/ATLAS-3.11.24/install/lib -Wl,-rpath,~/ATLAS-3.11.24/install/lib -latlas

disable-aslr:
	@echo "Disabling address randomization ..."
	sudo bash -c "echo 0 > /proc/sys/kernel/randomize_va_space"


A := 208 0 # Worstcase, A, x, y = (0x010, 0x010, 0x020)
B := 208 128 # Average, A, x, y -> (0x10, 0x010, 0x0b0)
C := 512 0 # Best, A, x, y -> (0x010, 0x140, 0x150)

# Do three invocations of lperf to measure performance for different memory
# addresses. Some tape and glue in bash to gather the results in a csv file
# `benchmark.csv` at the end.
# Case (a), (b), (c) with 1 iteration
# Case (a), (b), (c) with 101 iterations
# Separate counter names and mnemonics from first and second column.
# The order is preserved, so these columns are identical in each result.
benchmark: bin/gemv disable-aslr
	$(LPERF) -e $(PERFCOUNTERS) -r $(REPEAT) -n 1 $< $(A) 1 > lperf.a.1.csv 2> output.a.1.out 
	$(LPERF) -e $(PERFCOUNTERS) -r $(REPEAT) -n 1 $< $(B) 1 > lperf.b.1.csv 2> output.b.1.out 
	$(LPERF) -e $(PERFCOUNTERS) -r $(REPEAT) -n 1 $< $(C) 1 > lperf.c.1.csv 2> output.c.1.out

	$(LPERF) -e $(PERFCOUNTERS) -r $(REPEAT) -n 1 $< $(A) 101 > lperf.a.100.csv 2> output.a.100.out 
	$(LPERF) -e $(PERFCOUNTERS) -r $(REPEAT) -n 1 $< $(B) 101 > lperf.b.100.csv 2> output.b.100.out 
	$(LPERF) -e $(PERFCOUNTERS) -r $(REPEAT) -n 1 $< $(C) 101 > lperf.c.100.csv 2> output.c.100.out

	@cut -d ',' -f 1 lperf.a.1.csv > counters.tmp
	@cut -d ',' -f 2 lperf.a.1.csv > mnemonic.tmp

	@cut -d ',' -f 3 lperf.a.1.csv > a.1.tmp
	@cut -d ',' -f 3 lperf.b.1.csv > b.1.tmp
	@cut -d ',' -f 3 lperf.c.1.csv > c.1.tmp

	@cut -d ',' -f 3 lperf.a.100.csv > a.100.tmp
	@cut -d ',' -f 3 lperf.b.100.csv > b.100.tmp
	@cut -d ',' -f 3 lperf.c.100.csv > c.100.tmp

	@paste -d ',' counters.tmp mnemonic.tmp /dev/null a.1.tmp b.1.tmp c.1.tmp /dev/null a.100.tmp b.100.tmp c.100.tmp > benchmark.csv
	@rm *.tmp
	mv *.csv *.out bin



# axpy
bin/axpy: axpy.c
	cc -std=c11 $< -o $@ -I/usr/local/atlas/include -L/usr/local/atlas/lib -lsatlas

bin/axpy.csv: bin/axpy
	@echo "1 iteration" > $@
	$(LPERF) -e cycles:u,r0107:u --enumerate -r 100 -n 256 $< 1 >> $@ 2> /dev/null
	@echo "" >> $@
	@echo "101 iterations" >> $@
	$(LPERF) -e cycles:u,r0107:u --enumerate -r 100 -n 256 $< 101 >> $@ 2> /dev/null

	# Then fix formula in Calc and plot result. Clear spikes and correlation.


# Heatmap
bin/gemv-grid: gemv-grid.c
	gcc $< -o $@ -I/usr/local/atlas/include -L/usr/local/atlas/lib -lsatlas

bin/heatmap-alias.csv: bin/gemv-grid
	script/heatmap-create.py $< -x 256 -y 256 > $@

heatmap: bin/heatmap-alias.csv
	script/heatmap-plot.py --input $<
