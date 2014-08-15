	.file	"conv-restrict.c"
	.text
	.p2align 4,,15
	.globl	conv
	.type	conv, @function
conv:
.LFB0:
	.cfi_startproc
	cmpl	$4, %edi
	jle	.L1
	xorps	%xmm2, %xmm2
	subl	$5, %edi
	leaq	4(,%rdi,4), %r8
	xorl	%edi, %edi
	.p2align 4,,10
	.p2align 3
.L6:
	movaps	%xmm2, %xmm1
	leaq	(%rsi,%rdi), %rcx
	xorl	%eax, %eax
.L4:
	movss	(%rcx,%rax), %xmm0
	addq	$4, %rax
	mulss	k-4(%rax), %xmm0
	cmpq	$20, %rax
	addss	%xmm0, %xmm1
	jne	.L4
	movss	%xmm1, 8(%rdx,%rdi)
	addq	$4, %rdi
	cmpq	%r8, %rdi
	jne	.L6
.L1:
	rep ret
	.cfi_endproc
.LFE0:
	.size	conv, .-conv
	.section	.rodata
	.align 16
	.type	k, @object
	.size	k, 20
k:
	.long	1036831949
	.long	1048576000
	.long	1050253722
	.long	1048576000
	.long	1036831949
	.ident	"GCC: (Ubuntu 4.8.2-19ubuntu1) 4.8.2"
	.section	.note.GNU-stack,"",@progbits
