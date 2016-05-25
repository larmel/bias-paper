all: paper

paper: bin/paper.pdf

presentation: bin/presentation.pdf

clean:
	rm -f bin/*

bin:
	mkdir -p bin

about:
	uname -srvpi
	gcc --version

# Files that are used for plots, tables and listings in the article.
resources := \
	bin/microkernel-cycles-haswell.dat bin/microkernel-comparison-haswell.csv bin/microkernel-annotated.s \
	bin/microkernel-core.dat bin/microkernel-nehalem.dat bin/microkernel-ivybridge.dat \
	bin/conv-default-o2-haswell.estimate.dat bin/conv-default-o2-haswell.estimate.csv \
	bin/conv-default-o3-haswell.estimate.dat bin/conv-default-o3-haswell.estimate.csv \
	bin/convolution-kernel.c \
	bin/malloc-comparison.csv \
	bin/libblas.dat bin/libatlas.dat bin/libopenblas.dat

# Build in root to avoid trouble with pgfplots and output directories.
bin/paper.pdf: paper.tex references.bib $(resources) | bin
	latex paper.tex
	bibtex paper
	latex paper.tex
	latex paper.tex
	dvips -q -t letter -sDEVICE=pdfwrite paper.dvi
	ps2pdf paper.ps
	mv paper.pdf $@
	rm -f paper.log paper.dvi paper.ps paper.aux paper.bbl paper.blg paper.out

bin/presentation.pdf: presentation.tex $(resources) | bin
	latex $<
	bibtex presentation
	latex $<
	latex $<
	dvipdf presentation.dvi
	mv presentation.pdf $@
	rm -f presentation.aux presentation.dvi presentation.log presentation.out presentation.snm presentation.toc presentation.nav presentation.bbl presentation.blg presentation.vrb

# Gather results from analysis directory, but do some massaging to get
# the correct Tikz friendly format and filter out unnecessary data.

bin/microkernel-cycles-haswell.dat: analysis/environment/results-haswell/loop.csv | bin
	cat $< | util/select.py -e cycles:u | util/pgfpconv.py > $@

bin/microkernel-comparison-haswell.csv: analysis/environment/results-haswell/comparison.csv | bin
	cat $< \
		| util/select.py -e cycles:u,r0107:u,r020002a3:u,r01a2:u,r04a2:u,r04a1:u,r05a3:u,r08a1:u,r80a1:u,r10a1:u,r40a1:u,r01a1:u,r02a1:u,r20a1:u \
		> $@

bin/microkernel-core.dat: analysis/environment/results-core2/loop.csv | bin
	cat $< | util/select.py -e cycles:u,r0403:u,r0803:u | util/pgfpconv.py > $@

bin/microkernel-nehalem.dat: analysis/environment/results-nehalem/loop_i7-950_100p_alone_HT_r10.csv | bin
	cat $< | util/select.py -e cycles:u,r0107:u | util/pgfpconv.py > $@

bin/microkernel-ivybridge.dat: analysis/environment/results-ivybridge/loop_i5-3470_100p_alone_HT_r10.csv | bin
	cat $< | util/select.py -e cycles:u,r0107:u | util/pgfpconv.py > $@

bin/microkernel-annotated.s: analysis/environment/loop.s | bin
	cp $< $@

bin/convolution-kernel.c: analysis/heap-alias/conv.c | bin
	cp $< $@

bin/conv-default-o2-haswell.estimate.dat: analysis/heap-alias/results-haswell/default-o2.estimate.csv | bin
	cat $< | util/select.py -e cycles:u,r0107:u | util/pgfpconv.py > $@

bin/conv-default-o2-haswell.estimate.csv: analysis/heap-alias/results-haswell/default-o2.estimate.csv | bin
	$(eval positive := cycles:u,r01a2:u,r020002a3:u,r04a2:u,r01a1:u,r0107:u,r40a1:u,r05a3:u,r0160:u,rff88:u,r4188:u,r0860:u)
	$(eval cache := r01d1:u,r02d1:u,r08d1:u)
	cat $< | util/select.py -e $(positive) > $@

bin/conv-default-o3-haswell.estimate.dat: analysis/heap-alias/results-haswell/default-o3.estimate.csv | bin
	cat $< | util/select.py -e cycles:u,r0107:u | util/pgfpconv.py > $@

bin/conv-default-o3-haswell.estimate.csv: analysis/heap-alias/results-haswell/default-o3.estimate.csv | bin
	cat $< \
		| util/select.py -e cycles:u,r0107:u,r020002a3:u:u,r01a2:u,r04a2:u,r05a3:u,r0860:u,r20a1:u,r04a1:u,r0160:u \
		> $@

bin/malloc-comparison.csv: analysis/allocators/results/comparison.csv | bin
	cat $< > $@

bin/libblas.dat: analysis/blas/results-haswell-ht/libblas.estimate.csv | bin
	cat $< | util/select.py -e cycles:u,r0107:u | util/pgfpconv.py > $@

bin/libatlas.dat: analysis/blas/results-haswell-ht/libatlas.estimate.csv | bin
	cat $< | util/select.py -e cycles:u,r0107:u | util/pgfpconv.py > $@

bin/libopenblas.dat: analysis/blas/results-haswell-ht/libopenblas.estimate.csv | bin
	cat $< | util/select.py -e cycles:u,r0107:u | util/pgfpconv.py > $@

.PHONY: all paper presentation clean about
