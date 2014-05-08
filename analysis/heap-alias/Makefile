lperf := ../../util/lperf.py
estimate := ../../util/estimate.py
correlate := ../../util/correlate.py
lplot := ../../util/lplot.py

.PHONY: disable-aslr

disable-aslr:
	sudo bash -c "echo 0 > /proc/sys/kernel/randomize_va_space"


# Compile and optimize separately to avoid unwanted optimization to affect main

bin/main.o: main.c
	cc -c $< -o $@

# Compile convolution kernel in different configurations

bin/default.o: conv.c
	cc -c $< -o $@

bin/default-o1.o: conv.c
	cc -c $< -O1 -o $@

bin/default-o2.o: conv.c
	cc -c $< -O2 -o $@

bin/default-o3.o: conv.c
	cc -c $< -O3 -o $@

bin/default-o3-native.o: conv.c
	cc -c $< -O3 -march=native -o $@

bin/restrict-o3.o: conv-restrict.c
	cc -c $< -std=c99 -O3 -o $@

bin/restrict-o3-corei7.o: conv-restrict.c
	cc -c $< -std=c99 -march=corei7 -O3 -o $@


# Performance counter stats for 'bin/default 1 0':

#        90 006 878 cycles:u                  #    0,000 GHz                    
#         1 904 728 r0107:u                                                     
#       230 817 806 instructions:u            #    2,56  insns per cycle        

#       0,025686593 seconds time elapsed
bin/default: bin/main.o bin/default.o
	gcc $+ -o $@


# Performance counter stats for 'bin/default-o1 1 0':

#        54 633 535 cycles:u                  #    0,000 GHz                    
#        14 354 764 r0107:u                                                     
#       118 620 615 instructions:u            #    2,17  insns per cycle        

#       0,016609119 seconds time elapsed
bin/default-o1: bin/main.o bin/default-o1.o
	gcc $+ -o $@


# Performance counter stats for 'bin/default-o2 1 0':

#        49 915 070 cycles:u                  #    0,000 GHz                    
#        12 030 884 r0107:u                                                     
#       106 037 747 instructions:u            #    2,12  insns per cycle        

#       0,015085803 seconds time elapsed
bin/default-o2: bin/main.o bin/default-o2.o
	gcc $+ -o $@


# Performance counter stats for 'bin/default-o3 1 0':

#        40 515 894 cycles:u                  #    0,000 GHz                    
#         8 981 846 r0107:u                                                     
#        73 007 785 instructions:u            #    1,80  insns per cycle        

#       0,022412933 seconds time elapsed
bin/default-o3: bin/main.o bin/default-o3.o
	gcc $+ -o $@


# Performance counter stats for 'bin/default-o3-native 1 0':

#        35 457 226 cycles:u                  #    0,000 GHz                    
#         1 811 950 r0107:u                                                     
#        64 750 355 instructions:u            #    1,83  insns per cycle        

#       0,011715178 seconds time elapsed
bin/default-o3-native: bin/main.o bin/default-o3-native.o
	gcc $+ -o $@


# Performance counter stats for 'bin/restrict-o3 1 0':

#        32 496 212 cycles:u                  #    0,000 GHz                    
#           270 881 r0107:u                                                     
#        69 599 918 instructions:u            #    2,14  insns per cycle        

#       0,010533973 seconds time elapsed
bin/restrict-o3: bin/main.o bin/restrict-o3.o
	gcc $+ -o $@


# Performance counter stats for 'bin/restrict-o3-corei7 1 0':

#        32 126 262 cycles:u                  #    0,000 GHz                    
#           225 402 r0107:u                                                     
#        68 027 072 instructions:u            #    2,12  insns per cycle        

#       0,010556418 seconds time elapsed
bin/restrict-o3-corei7: bin/main.o bin/restrict-o3-corei7.o
	gcc $+ -o $@



# Measure all counters for 32 different heap offsets

bin/%.1.csv: bin/% disable-aslr
	$(lperf) -e all -n 32 -r 10 --env-increment 0 --enumerate $< 1 > $@

bin/%.11.csv: bin/% disable-aslr
	$(lperf) -e all -n 32 -r 10 --env-increment 0 --enumerate $< 11 > $@

bin/%.estimate.csv: bin/%.11.csv bin/%.1.csv
	$(estimate) --delta 10 --longrun $< --shortrun $(word 2,$^) | $(correlate) cycles:u > $@


# For debug purposes, find interesting scenarios
bin/%.quick-estimate.csv: bin/% disable-aslr
	$(lperf) -e cycles:u,r0107:u -n 32 -r 1 --env-increment 0 --enumerate $< 1 > bin/a.csv
	$(lperf) -e cycles:u,r0107:u -n 32 -r 1 --env-increment 0 --enumerate $< 11 > bin/b.csv
	$(estimate) --delta 10 --longrun bin/b.csv --shortrun bin/a.csv > $@
	rm bin/a.csv bin/b.csv
	$(lplot) --input $@


# Measure only cycles and alias for the full 4k offset (400 floats)
bin/%.4k.csv: bin/% disable-aslr
	$(lperf) -e cycles:u,r0107:u -n 400 -r 1 --env-increment 0 --enumerate $< 1 > $@
