
Analysis of aliasing in `Loop` microkernel
==========================================

Vanilla implementation is found in `loop.c`. This file contains a C program that is more or less equivalent to a microkernel that was first presented by Mytkoviz et al in "Producing Wrong Data Without Doing Anything Obviously Wrong".

The following command is useful for controlling environment size when running perf stat.
The env size is 3200 + 3 (X, =, \0), plus whatever is added by perf. Variables
added by perf includes PWD and PATH, about 170 B total for test config.

Should be exactly the same behavior as starting with `process.Popen(env={..})` from lperf.

    $ env -i X=`head -c 3200 </dev/zero | tr '\0' '0'` perf stat -e cycles:u,r0107:u ./analysis
    7fffffffe03c 7fffffffe038 

     Performance counter stats for './analysis':

                835549 cycles:u                  #    0.000 GHz                    
                327893 r0107:u                                                     
