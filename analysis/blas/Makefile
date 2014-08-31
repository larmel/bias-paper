lperf := ../../util/lperf.py
estimate := ../../util/estimate.py
correlate := ../../util/correlate.py

disable-aslr:
	@echo "Disabling address randomization ..."
	sudo bash -c "echo 0 > /proc/sys/kernel/randomize_va_space"

# Standard blas alternatives (not custom compiled)

# Link to default package, assumed to be libblas
bin/gemv-libblas: gemv-mmap.c
	gcc $< -o $@ -lblas

# apt-get install libatlas3-base libatlas-base-dev
bin/gemv-libatlas: gemv-mmap.c
	gcc $< /usr/lib/atlas-base/libcblas.a /usr/lib/atlas-base/libatlas.a -o $@

# apt-get install libopenblas-base libopenblas-dev
bin/gemv-libopenblas: gemv-mmap.c
	gcc $< /usr/lib/openblas-base/libblas.a -o $@ -lpthread


repeat = 100

bin/%.1.csv: bin/gemv-% | disable-aslr
	$(lperf) -e all --enumerate -r $(repeat) -n 16 $< 1 0 > $@

bin/%.11.csv: bin/gemv-% | disable-aslr
	$(lperf) -e all --enumerate -r $(repeat) -n 16 $< 11 0 > $@

bin/libblas.estimate.csv: bin/libblas.11.csv bin/libblas.1.csv
	$(estimate) --delta 10 --longrun $< --shortrun $(word 2,$^) | $(correlate) cycles:u > $@

bin/libatlas.estimate.csv: bin/libatlas.11.csv bin/libatlas.1.csv
	$(estimate) --delta 10 --longrun $< --shortrun $(word 2,$^) | $(correlate) cycles:u > $@

bin/libopenblas.estimate.csv: bin/libopenblas.11.csv bin/libopenblas.1.csv
	$(estimate) --delta 10 --longrun $< --shortrun $(word 2,$^) | $(correlate) cycles:u > $@

results: bin/libblas.1.csv bin/libblas.11.csv bin/libblas.estimate.csv \
	bin/libatlas.1.csv bin/libatlas.11.csv bin/libatlas.estimate.csv \
	bin/libopenblas.1.csv bin/libopenblas.11.csv bin/libopenblas.estimate.csv


.PHONY: disable-aslr results
