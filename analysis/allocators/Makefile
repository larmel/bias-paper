.PHONY: test disable-aslr
.DEFAULT: bin/heapalloc

disable-aslr:
	sudo bash -c 'echo 0 > /proc/sys/kernel/randomize_va_space'

test: bin/malloc-comparison.csv

bin:
	mkdir -p bin

bin/heapalloc: heapalloc.c | bin
	cc heapalloc.c -o $@

bin/ptmalloc.csv: bin/heapalloc disable-aslr
	@echo "size,ptmalloc," > $@
	bin/heapalloc >> $@

bin/tcmalloc.csv: bin/heapalloc disable-aslr
	@echo "size,tcmalloc," > $@
	LD_PRELOAD=/usr/lib/libtcmalloc_minimal.so.4 bin/heapalloc >> $@

bin/jemalloc.csv: bin/heapalloc disable-aslr
	@echo "size,jemalloc," > $@
	LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libjemalloc.so.1 bin/heapalloc >> $@

bin/hoard.csv: bin/heapalloc disable-aslr
	@echo "size,hoard," > $@
	LD_PRELOAD=bin/libhoard.so bin/heapalloc >> $@

bin/malloc-comparison.csv: bin/ptmalloc.csv bin/tcmalloc.csv bin/jemalloc.csv bin/hoard.csv
	paste $+ > $@
