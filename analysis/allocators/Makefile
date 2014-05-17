SHELL := /bin/bash
.PHONY: results disable-aslr

bin/heapalloc: heapalloc.c | bin
	cc heapalloc.c -o $@

disable-aslr:
	sudo bash -c 'echo 0 > /proc/sys/kernel/randomize_va_space'

bin:
	mkdir -p bin

bin/ptmalloc.csv: bin/heapalloc | disable-aslr
	#@echo ",64,1024,5120,1048576" > $@
	@echo -n "glibc (ptmalloc)," > $@
	bin/heapalloc 64 		>> $@ && echo -n "," >> $@
	bin/heapalloc 1024 		>> $@ && echo -n "," >> $@
	bin/heapalloc 5120 		>> $@ && echo -n "," >> $@
	bin/heapalloc 1048576 	>> $@ 
	@echo "" >> $@

bin/tcmalloc.csv: bin/heapalloc | disable-aslr
	#@echo ",64,1024,5120,1048576" > $@
	@echo -n "tcmalloc," > $@
	LD_PRELOAD=/usr/lib/libtcmalloc_minimal.so.4 bin/heapalloc 64 		>> $@ && echo -n "," >> $@
	LD_PRELOAD=/usr/lib/libtcmalloc_minimal.so.4 bin/heapalloc 1024 	>> $@ && echo -n "," >> $@
	LD_PRELOAD=/usr/lib/libtcmalloc_minimal.so.4 bin/heapalloc 5120 	>> $@ && echo -n "," >> $@
	LD_PRELOAD=/usr/lib/libtcmalloc_minimal.so.4 bin/heapalloc 1048576 	>> $@ 
	@echo "" >> $@

	# @echo "size,tcmalloc," > $@
	# LD_PRELOAD=/usr/lib/libtcmalloc_minimal.so.4 bin/heapalloc >> $@

bin/jemalloc.csv: bin/heapalloc | disable-aslr
	#@echo ",64,1024,5120,1048576" > $@
	@echo -n "jemalloc," > $@
	LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libjemalloc.so.1 bin/heapalloc 64 		>> $@ && echo -n "," >> $@
	LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libjemalloc.so.1 bin/heapalloc 1024 	>> $@ && echo -n "," >> $@
	LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libjemalloc.so.1 bin/heapalloc 5120 	>> $@ && echo -n "," >> $@
	LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libjemalloc.so.1 bin/heapalloc 1048576 >> $@ 
	@echo "" >> $@
	# @echo "size,jemalloc," > $@
	# LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libjemalloc.so.1 bin/heapalloc >> $@

bin/hoard.csv: bin/heapalloc disable-aslr
	#@echo ",64,1024,5120,1048576" > $@
	@echo -n "Hoard," > $@
	LD_PRELOAD=bin/libhoard.so bin/heapalloc 64 	>> $@ && echo -n "," >> $@
	LD_PRELOAD=bin/libhoard.so bin/heapalloc 1024 	>> $@ && echo -n "," >> $@
	LD_PRELOAD=bin/libhoard.so bin/heapalloc 5120 	>> $@ && echo -n "," >> $@
	LD_PRELOAD=bin/libhoard.so bin/heapalloc 1048576 >> $@ 
	@echo "" >> $@
	# @echo "size,hoard," > $@
	# LD_PRELOAD=bin/libhoard.so bin/heapalloc >> $@

bin/comparison.csv: bin/ptmalloc.csv bin/tcmalloc.csv bin/jemalloc.csv bin/hoard.csv
	@echo "Allocation,64,1024,5120,1048576" > $@
	paste --serial $+ >> $@

results: bin/comparison.csv
