
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

