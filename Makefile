.PHONY: all paper disable-aslr clean about

all: paper

paper: bin/paper.pdf

disable-aslr:
	@echo "Disabling address randomization ..."
	sudo bash -c "echo 0 > /proc/sys/kernel/randomize_va_space"

clean:
	rm -f bin/*

bin:
	mkdir -p bin

about:
	uname -srvpi
	gcc --version

# Files that are used for plots, tables and listings in the article.
resources := bin/micro-kernel-cycles.dat bin/micro-kernel-comparison.csv bin/micro-kernel-annotated.s \
	bin/conv-default-o2.estimate.dat bin/conv-default-o2.estimate.csv \
	bin/conv-default-o3.estimate.dat bin/conv-default-o3.estimate.csv \
	bin/convolution-kernel.c

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

bin/micro-kernel-cycles.dat: analysis/env-alias/results/cycles.csv | bin
	cat $< | util/pgfpconv.py > $@

bin/micro-kernel-comparison.csv: analysis/env-alias/results/comparison.csv | bin
	cat $< \
		| util/select.py -e cycles:u,r0107:u,r02a3:u,r01a2:u,r04a2:u,r04a1:u,r05a3:u,r08a1:u,r80a1:u,r10a1:u,r40a1:u,r01a1:u,r02a1:u,r20a1:u \
		> $@

bin/micro-kernel-annotated.s: analysis/env-alias/loop.s | bin
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
