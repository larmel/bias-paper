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

plotfiles := bin/micro-kernel-cycles.dat bin/micro-kernel-comparison.csv bin/default-o3.estimate.dat

# Move and process data files for inclusion in the paper

bin/micro-kernel-cycles.dat: analysis/env-alias/results/cycles.csv | bin
	cat $< | util/pgfpconv.py > $@

bin/micro-kernel-comparison.csv: analysis/env-alias/results/comparison.csv | bin
	cat $< \
		| util/select.py -e cycles:u,bus-cycles:u,r0107:u,r02a3:u,r01a2:u,r04a2:u,r025c:u,r04a1:u,r05a3:u,r08a1:u,r80a1:u,r10a1:u,r40a1:u,r01a1:u,r02a1:u,r20a1:u \
		> $@

# Build in root to avoid trouble with pgfplots and output directories.
bin/paper.pdf: paper.tex references.bib $(plotfiles) | bin
	latex paper.tex
	bibtex paper
	latex paper.tex
	latex paper.tex
	dvipdf paper.dvi
	mv paper.pdf $@
	rm -f paper.log paper.dvi paper.aux paper.bbl paper.blg
