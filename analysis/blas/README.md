
Analysis of Aliasing in BLAS libraries
======================================


Setup and Installation of ATLAS
-------------------------------

Version 3.10.1 does not recognize Haswell chips in the configure step. A fix was apparently added in [3.11.15](http://sourceforge.net/p/math-atlas/support-requests/913/). 

Get one config error, about xctest not found. The exact same error on both the stable release and latest dev. Not sure what that is..



    make atlas_run atldir=/home/lars/ATLAS-3.11.24/install exe=xprobe_comp redir=config1.out \
                    args="-v 0 -o atlconf.txt -O 1 -A 28 -Si nof77 0 -V 976   -b 64 -d b /home/lars/ATLAS-3.11.24/install"
    make[1]: Entering directory `/home/lars/ATLAS-3.11.24/install'
    cd /home/lars/ATLAS-3.11.24/install ; ./xprobe_comp -v 0 -o atlconf.txt -O 1 -A 28 -Si nof77 0 -V 976   -b 64 -d b /home/lars/ATLAS-3.11.24/install > config1.out
    /bin/sh: 1: ./xctest: not found
    make[3]: *** [atlas_run] Error 127
    make[2]: *** [IRunCComp] Error 2
    probe_f2c.o: In function `ATL_tmpnam':



Source files were retrieved from [sourceforge](http://sourceforge.net/projects/math-atlas/files/). At the time of writing, the latest stable version is 3.10.1, and the latest experimental version is 3.11.15. Disable CPU frequency scaling by choosing 'performance' option in indicator-cpufreq. This setting is checked in the configure script. As always, we have hyperthreading disabled. GCC version used for compilation: gcc (Ubuntu/Linaro 4.8.1-10ubuntu9) 4.8.1. 
See atlas_install.pdf for official documentation on installation. This section outlines the exact parameters that were used for our experiments. 

Prerequisites:
apt-get install gfortran

 1. Download archive atlas3.10.1.tar.bz2 and extract into ~/ATLAS
 2. `cd ~/ATLAS`
 3. `mkdir install; cd install`
 4. `../configure --shared` In case of errors, just run rm -fr *, resolve and try again. 
 5. `make`              tune and compile library
 6. `make check`        perform sanity tests
 7. `make ptcheck`      checks of threaded code for multiprocessor systems
 8. `make time`         provide performance summary as % of clock rate
 9. `make install`      Copy library and include files to other directories


Library is installed to /usr/local/atlas by default. This is the output of `time` target. The reference BLAS was the default one bundled with the OS.

    Reference clock rate=3500Mhz, new rate=3501Mhz
       Refrenc : % of clock rate achieved by reference install
       Present : % of clock rate achieved by present ATLAS install

                        single precision                  double precision
                ********************************   *******************************
                      real           complex           real           complex
                ---------------  ---------------  ---------------  ---------------
    Benchmark   Refrenc Present  Refrenc Present  Refrenc Present  Refrenc Present
    =========   ======= =======  ======= =======  ======= =======  ======= =======
      kSelMM     1454.9  1574.0   1292.6  1385.6    761.7   822.9    697.9   752.7
      kGenMM      349.9   375.0    348.9   376.6    339.7   364.8    315.4   336.2
      kMM_NT      342.0   354.9    341.8   364.5    322.9   345.7    313.2   326.8
      kMM_TN      335.3   353.5    331.3   354.8    318.8   332.6    301.0   319.0
      BIG_MM     2951.9  3109.8   3122.3  3115.3   1518.3  1554.3   1540.2  1535.7
       kMV_N      228.5   276.3    453.8   449.6    109.9   119.8    217.2   204.6
       kMV_T      225.8   253.4    476.9   509.5    119.4   113.3    232.5   209.2
        kGER      164.7   160.0    315.5   312.0     78.4    65.7    158.8   140.5



Other BLAS packages
-------------------

Some info on swithing in this [blogpost](http://www.stat.cmu.edu/~nmv/2013/07/09/for-faster-r-use-openblas-instead-better-than-atlas-trivial-to-switch-to-on-ubuntu/). `apt-cache search libblas` should give at least three alternatives:

 *  `libblas`
  By default only compiled share library is present. Need libblas-dev to get cblas.h (and cblas_f77.h)

 *  `libatlas`
  Pre-compiled implementation of ATLAS. This does not use auto-tuning which potentially could fix aliasing.

 *  `libopenblas`


Generating heatmap in R
-----------------------

install.packages("lattice")

```
library(lattice)
trellis.par.set(canonical.theme(color = FALSE))
tmp <- read.csv("heatmap-alias.csv", sep=",", header=FALSE)
m <- as.matrix(tmp)
setEPS()
postscript("heatmap.eps", family="Computer Modern")
levelplot(m, pretty=TRUE, scales=list(draw=F), xlab="x vector address offset times 0x10", ylab="y vector address offset times 0x10")
dev.off()
```

With tikzDevice

install.packages("tikzDevice")

```
library(lattice)
require(tikzDevice)
trellis.par.set(canonical.theme(color = FALSE))
tmp <- read.csv("heatmap-alias.csv", sep=",", header=FALSE)
m <- as.matrix(tmp)
tikz("heatmap.tex", standAlone=TRUE, width=5, height=5)
levelplot(m, pretty=TRUE, scales=list(draw=F), xlab="x vector address offset times 0x10", ylab="y vector address offset times 0x10")
dev.off()
```

Then 150k lines of tikz commands. pdflatex gives up, can use luatex instead.



Random notes on perf testing
----------------------------

Observed that aliasing in gemv-grid was not completely deterministic for seemingly "good" offsets. Ex. for dy = 0 sometimes spikes enormously (for 8192 x 8192). No issues with ASLR disabled.

Need to understand startup cost of memory allocation better. Cycle count dramatically reduces when
given -r option (For 64 x 64 matrix).

    lars@Berlin:~/bias-paper/analysis/blas$ perf stat -e cycles:u,r0107:u -r 100 bin/gemv-grid 0 0 1

     Performance counter stats for 'bin/gemv-grid 0 0 1' (100 runs):

             2 209 440 cycles:u                  #    0,000 GHz                      ( +-  1,19% )
                 5 175 r0107:u                                                       ( +-  0,60% )

           0,001056276 seconds time elapsed                                          ( +-  3,63% )

    lars@Berlin:~/bias-paper/analysis/blas$ perf stat -e cycles:u,r0107:u -r 1 bin/gemv-grid 0 0 1

     Performance counter stats for 'bin/gemv-grid 0 0 1':

             3 504 587 cycles:u                  #    0,000 GHz                    
                 6 421 r0107:u                                                     

           0,001660842 seconds time elapsed

Ok, this actually solves it. No idea why. Warmup of branch prediction?

    for i in {1..100}; do bin/gemv-grid; done && perf stat -e cycles:u,r0107:u -r 1 bin/gemv-grid 0 0 1


