
.PHONY: all paper data disable-aslr clean

# Default to generating just the paper, given existing data in resources.
all: paper

# Compile examples and perform all measurements needed. Everyting is put in bin
# folder, so if you actually want to update things in the article it has to be 
# copied manually to the resources folder.
data: bin/stack-offset.csv bin/convolution.csv

paper: bin/paper.pdf

disable-aslr:
	@echo "Disabling address randomization ..."
	sudo bash -c "echo 0 > /proc/sys/kernel/randomize_va_space"

clean:
	rm -f bin/*

bin:
	mkdir -p bin

# Print information about current platform, including version of various
# software
about:
	uname -srvpi
	gcc --version


plotfiles = bin/convolution.dat bin/stack-offset.dat bin/conv-all-estimate.dat

# Build in root to avoid trouble with pgfplots and output directories.
bin/paper.pdf: paper.tex references.bib $(plotfiles) | bin
	latex paper.tex
	bibtex paper
	latex paper.tex
	latex paper.tex
	dvipdf paper.dvi
	mv paper.pdf $@
	rm -f paper.log paper.dvi paper.aux paper.bbl paper.blg

# Generate TiKz plot format from raw performance counter results. Nothing in
# resources is generated, and must be updated manually.
bin/%.dat: resources/%.csv | bin
	cat $+ | util/pgfpconv.py > $@




# Section that produces resource files and raw data used in the article
#

# todo: probably remove this

bin/stack-offset.csv: disable-aslr bin/loop
	util/lperf -e cycles:u,r0107:u,r01a2:u,r02a3:u -n 512 -r 100 --env-increment 16 bin/loop > $@

bin/loop-recursion-fix.csv: disable-aslr bin/loop-recursion-fix
	util/lperf -e cycles:u,r0107:u,r01a2:u,r02a3:u -n 512 -r 100 --env-increment 16 bin/loop-recursion-fix > $@

# Hard-coded offset that hits around worst case on our machine. Warning: This 
# takes a long time.
bin/stack-offset-all.csv: disable-aslr bin/loop
	util/lperf -e all -n 300 -r 100 --env-increment 1 --env-offset 3100 bin/loop > $@

bin/loop: code/env-alias/loop.c
	cc $+ -o $@

bin/loop-recursion-fix: code/env-alias/loop-recursion-fix.c
	cc $+ -o $@

bin/convolution.csv: disable-aslr bin/convolution
	util/lperf -e cycles:u,r0107:u -n 32 -r 100 --env-increment 0 --enumerate bin/convolution > $@

bin/convolution: code/heap-alias/convolution.c
	cc -O3 $+ -o $@


