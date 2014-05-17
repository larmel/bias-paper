.PHONY: results disable-aslr

results: bin/comparison.csv

disable-aslr:
	sudo bash -c 'echo 0 > /proc/sys/kernel/randomize_va_space'

bin:
	mkdir -p bin

bin/heapalloc: heapalloc.c | bin
	cc heapalloc.c -o $@

# Run heapalloc for different allocation sizes, pasting together the results.
sizes := 64 1024 5120 65536 1048576 4194304

bin/ptmalloc.csv: bin/heapalloc | disable-aslr
	for n in $(sizes) ; do \
		$< $$n > bin/$$n.tmp ; \
	done
	echo "glibc" > bin/header.tmp
	echo "(ptmalloc)" >> bin/header.tmp
	paste -d "," bin/header.tmp $(addprefix bin/,$(addsuffix .tmp,$(sizes))) > $@
	rm bin/*.tmp

bin/tcmalloc.csv: bin/heapalloc | disable-aslr
	for n in $(sizes) ; do \
		LD_PRELOAD=/usr/lib/libtcmalloc_minimal.so.4 $< $$n > bin/$$n.tmp ; \
	done
	@echo "tcmalloc" > bin/header.tmp
	paste -d "," bin/header.tmp $(addprefix bin/,$(addsuffix .tmp,$(sizes))) > $@
	rm bin/*.tmp

bin/jemalloc.csv: bin/heapalloc | disable-aslr
	for n in $(sizes) ; do \
		LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libjemalloc.so.1 $< $$n > bin/$$n.tmp ; \
	done
	echo "jemalloc" > bin/header.tmp
	paste -d "," bin/header.tmp $(addprefix bin/,$(addsuffix .tmp,$(sizes))) > $@
	rm bin/*.tmp

bin/hoard.csv: bin/heapalloc | disable-aslr
	for n in $(sizes) ; do \
		LD_PRELOAD=bin/libhoard.so $< $$n > bin/$$n.tmp ; \
	done
	echo "Hoard" > bin/header.tmp
	paste -d "," bin/header.tmp $(addprefix bin/,$(addsuffix .tmp,$(sizes))) > $@
	rm bin/*.tmp

comma:= ,
empty:=
space:= $(empty) $(empty)

bin/comparison.csv: bin/ptmalloc.csv bin/tcmalloc.csv bin/jemalloc.csv bin/hoard.csv
	echo -n "Allocation," > $@
	echo $(subst $(space),$(comma),$(sizes)) >> $@
	cat $+ >> $@
