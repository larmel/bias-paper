
Analysis of aliasing in `Loop` microkernel
==========================================

Vanilla implementation is found in `loop.c`. This file contains a C program that is more or less equivalent to a *microkernel* that was first presented by Mytkoviz et al in "Producing Wrong Data Without Doing Anything Obviously Wrong". 


Measurements
------------

This command is useful for controlling environment size when running perf stat.
The env size is 3200 + 3 (X, =, \0), plus whatever is added by perf. Variables
added by perf includes PWD and PATH, about 170 B total for test config.

Should be exactly the same behavior as starting with process.Popen(env={..}).

```$ env -i X=`head -c 3200 </dev/zero | tr '\0' '0'` perf stat -e cycles:u,r0107:u ./analysis
7fffffffe03c 7fffffffe038 

 Performance counter stats for './analysis':

            835549 cycles:u                  #    0.000 GHz                    
            327893 r0107:u                                                     
```


Attempted gdb approach
----------------------

Workflow for trying to verify dynamic addresses of inc and g using gdb. Assumption is
that size of environment variables and stack start address must be the same
both in and outside of gdb. 

Generate a string of '0' characters for environment in normal shell, copy to 
set gdb environment later. The correct environment size to generate alias will
vary between setups. Address for breakpoint depends from compiler, as do access
to g and inc.

Note that even though one unsets the environment, PWD and SHLVL vars are still
set by gdb. Running ./printenv shows a difference of 0x60 in stack start
address between gdb envsize 49 and env -i X=... ./printenv. Gdb starts at 
0x7fffffffec20, env -i at 0x7fffffffec80. There is probably some extra stuff
on top of stack added by gdb. 

```
sudo bash -c "echo 0 > /proc/sys/kernel/randomize_va_space"
head -c 3200 </dev/zero | tr '\0' '0'

gdb loop
unset environment
set environment X 000000...
break *0x4004ff
run
x/ $rbp-0x8
x/ $rbp-0x4
```

```00000000004004ed <main>:
  4004ed:	55                   	push   %rbp
  4004ee:	48 89 e5             	mov    %rsp,%rbp
  4004f1:	c7 45 f8 00 00 00 00 	movl   $0x0,-0x8(%rbp)
  4004f8:	c7 45 fc 01 00 00 00 	movl   $0x1,-0x4(%rbp)
  4004ff:	eb 37                	jmp    400538 <main+0x4b>
```
