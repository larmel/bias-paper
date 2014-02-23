This is a small test scenario to look at the differences (if any) in the addresses returned by some common heap allocators. 
Replacements are injected using the LD\_PRELOAD environment variable. Paths of .so files might vary.


 *	**ptmalloc** (glibc)  
	Online [documentation](http://www.gnu.org/software/libc/manual/html_mono/libc.html).

	    /lib/x86_64-linux-gnu/libc.so.6 
	    GNU C Library (Ubuntu EGLIBC 2.17-93ubuntu4) stable release version 2.17, by Roland McGrath et al.
	    Copyright (C) 2012 Free Software Foundation, Inc.


 *	**tcmalloc**  

 	`apt-get install libtcmalloc-minimal4`

	`LD_PRELOAD=/usr/lib/libtcmalloc_minimal.so.4`


 *	**jemalloc**  

	`apt-get install libjemalloc1`  
	> jemalloc is a general-purpose scalable concurrent malloc(3) implementation.
	> This distribution is a "portable" implementation that currently targets
	> FreeBSD, Linux, Apple OS X, and MinGW. jemalloc is included as the default
	> allocator in the FreeBSD and NetBSD operating systems, and it is used by the
	> Mozilla Firefox web browser on Microsoft Windows-related platforms. (README)

 	`LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libjemalloc.so.1`

 	More information: [whitepaper](http://people.freebsd.org/~jasone/jemalloc/bsdcan2006/jemalloc.pdf)


 *	**Hoard**  
	Download binary from [hoard.org](http://www.hoard.org/), extract libhoard.so in bin directory.

	`LD_PRELOAD=bin/libhoard.so`


