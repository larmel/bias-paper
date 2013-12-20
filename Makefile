
.PHONY: all paper disable-aslr clean

# Default to generating just the paper
all: paper


paper: bin/paper.pdf

# Files needed for TikZ plots
plotdata = resources/motivation.dat resources/stack-offset.dat bin/convolution.dat

#
# Build in root to avoid trouble with pgfplots and output directories
bin/paper.pdf: paper.tex references.bib $(plotdata)
	latex paper.tex
	bibtex paper
	latex paper.tex
	latex paper.tex
	dvipdf paper.dvi
	mv paper.pdf $@
	rm -f paper.log paper.dvi paper.aux paper.bbl paper.blg

# Resources for TikZ
# Things in resources are assumed to be checked in to version control
# TODO: This should be in bin as well
resources/%.dat: resources/%.csv
	cat $+ | util/pgfpconv > $@

# New style
bin/%.dat: bin/%.csv
	cat $+ | util/pgfpconv > $@

#
# Performance counter measurements
bin/stack-offset.csv: code/loop/loop
	util/lperf $+ -e cycles:u,r0107:u,r01a2:u,r02a3:u -n 512 -r 100 --env-increment 16 > $@

bin/convolution.csv: bin/convolution
	util/lperf $+ -e cycles:u,r0107:u -n 32 -r 100 --arg-increment 1 --env-increment 0 > $@


#
# Build microkernel code
bin/convolution: code/heap-alias/convolution.c
	cc -O3 $+ -o $@


# Make sure stack, mmap and heap sections have fixed addresses between each run.
# Needed for reproducible measurements when measuring impact of environment size.
disable-aslr:
	@echo "Disabling address randomization"
	sudo bash -c "echo 0 > /proc/sys/kernel/randomize_va_space"

#
# Remove every auto-generated file
clean:
	rm -f bin/*

