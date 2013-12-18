
.PHONY: all paper clean

# Default to generating just the paper
all: paper


paper: bin/paper.pdf

# Files needed for TikZ plots
plotdata = resources/motivation.dat resources/stack-offset.dat

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
resources/%.dat: resources/%.csv
	cat $+ | util/pgfpconv > $@

#
# Performance counter measurements, put in bin
bin/stack-offset.csv: code/loop/loop
	util/lperf $+ -e cycles:u,r0107:u,r01a2:u,r02a3:u -n 512 -r 100 --env-increment 16 \
		> $@





#
# Remove every auto-generated file
clean:
	rm -f bin/*
	rm -f resources/*.dat

