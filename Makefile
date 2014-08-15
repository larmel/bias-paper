.PHONY: all paper clean about

all: paper

paper: bin/paper.pdf

clean:
	rm -f bin/*

bin:
	mkdir -p bin

about:
	uname -srvpi
	gcc --version

# Files that are used for plots, tables and listings in the article.
resources := bin/microkernel-cycles-core2.dat \
	bin/microkernel-cycles-haswell.dat bin/microkernel-comparison-haswell.csv bin/microkernel-annotated.s \
	bin/conv-default-o2.estimate.dat bin/conv-default-o2.estimate.csv \
	bin/conv-default-o3.estimate.dat bin/conv-default-o3.estimate.csv \
	bin/convolution-kernel.c \
	bin/malloc-comparison.csv

# Build in root to avoid trouble with pgfplots and output directories.
bin/paper.pdf: paper.tex references.bib $(resources) | bin
	latex paper.tex
	bibtex paper
	latex paper.tex
	latex paper.tex
	dvipdf paper.dvi
	mv paper.pdf $@
	rm -f paper.log paper.dvi paper.aux paper.bbl paper.blg

#
# Depend on results from analysis directory, but do some massaging to get the
# correct Tikz friendly format and filter out unnecessary data.

bin/microkernel-cycles-core2.dat: analysis/environment/results-core2/loop.csv | bin
	cat $< | util/select.py -e cycles:u | util/pgfpconv.py > $@

bin/microkernel-cycles-haswell.dat: analysis/environment/results-haswell/loop.csv | bin
	cat $< | util/select.py -e cycles:u | util/pgfpconv.py > $@

bin/microkernel-comparison-haswell.csv: analysis/environment/results-haswell/comparison.csv | bin
	cat $< \
		| util/select.py -e cycles:u,r0107:u,r020002a3:u,r01a2:u,r04a2:u,r04a1:u,r05a3:u,r08a1:u,r80a1:u,r10a1:u,r40a1:u,r01a1:u,r02a1:u,r20a1:u \
		> $@

bin/microkernel-annotated.s: analysis/environment/loop.s | bin
	cp $< $@

bin/convolution-kernel.c: analysis/heap-alias/conv.c | bin
	cp $< $@

bin/conv-default-o2.estimate.dat: analysis/heap-alias/results/default-o2.estimate.csv | bin
	cat $< | util/select.py -e cycles:u,r0107:u | util/pgfpconv.py > $@

bin/conv-default-o2.estimate.csv: analysis/heap-alias/results/default-o2.estimate.csv | bin
	$(eval positive := cycles:u,r01a2:u,r02a3:u,r04a2:u,r01a1:u,r0107:u,r40a1:u,r05a3:u,r0160:u,rff88:u,r4188:u,r0860:u)
	$(eval cache := r01d1:u,r02d1:u,r08d1:u)
	cat $< | util/select.py -e $(positive) > $@

bin/conv-default-o3.estimate.dat: analysis/heap-alias/results/default-o3.estimate.csv | bin
	cat $< | util/select.py -e cycles:u,r0107:u | util/pgfpconv.py > $@

bin/conv-default-o3.estimate.csv: analysis/heap-alias/results/default-o3.estimate.csv | bin
	cat $< \
		| util/select.py -e cycles:u,r0107:u,r02a3:u,r01a2:u,r04a2:u,r05a3:u,r0860:u,r20a1:u,r04a1:u,r0160:u \
		> $@

bin/malloc-comparison.csv: analysis/allocators/results/comparison.csv | bin
	cat $< > $@
