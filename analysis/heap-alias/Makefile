
lperf := ../../util/lperf

# Don't delete intermediate csv files
.SECONDARY: bin/%.csv
.PHONY: disable-aslr

disable-aslr:
	sudo bash -c "echo 0 > /proc/sys/kernel/randomize_va_space"




# Make binaries

bin/conv-gcc-0: convolution.c
	cc $+ -o $@

bin/conv-gcc-3: convolution.c
	cc -O3 $+ -o $@

bin/conv-optimized-gcc-3: convolution-optimized.c
	cc -O3 $+ -o $@

# Compile and optimize separately to avoid unwanted optimization to affect main
bin/conv: conv.c main.c
	cc -c conv.c -O3 -o bin/conv.o
	cc -c main.c -o bin/main.o
	gcc bin/conv.o bin/main.o -o bin/conv


# Measure for increasing offsets for each binary. Pattern matching rule to
# cover all possible compiled versions.
# Example: make bin/conv-gcc-estimate.csv
# Nb: Must invoke disable-aslr before this

bin/%-11.csv: bin/%
	$(lperf) -e cycles:u,r0107:u -n 32 -r 1 --env-increment 0 --enumerate $< 11 > $@

bin/%-1.csv: bin/%
	$(lperf) -e cycles:u,r0107:u -n 32 -r 1 --env-increment 0 --enumerate $< 1 > $@

bin/%-estimate.csv: bin/%-11.csv bin/%-1.csv
	./estimate.py --delta 10 --longrun $< --shortrun $(word 2,$^) > $@


bin/%-all-1.csv: bin/%
	$(lperf) -e all --correlate cycles:u -n 32 -r 1 --env-increment 0 --enumerate $< 1 > $@
