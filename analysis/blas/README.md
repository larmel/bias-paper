
Analysis of Aliasing in BLAS libraries
======================================

Switching blas package
----------------------

Some info on swithing in this [blogpost](http://www.stat.cmu.edu/~nmv/2013/07/09/for-faster-r-use-openblas-instead-better-than-atlas-trivial-to-switch-to-on-ubuntu/). `apt-cache search libblas` should give at least three alternatives:

 *	`libblas`
	By default only compiled share library is present. Need libblas-dev to get cblas.h (and cblas_f77.h)

 *	`libatlas`
	Pre-compiled implementation of ATLAS. This does not use auto-tuning which potentially could fix aliasing.

 * 	`libopenblas`

