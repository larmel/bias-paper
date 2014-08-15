	.file	"conv.c"
	.text
	.p2align 4,,15
	.globl	conv
	.type	conv, @function
conv:
.LFB0:
	.cfi_startproc
	leal	-2(%rdi), %r8d
	cmpl	$2, %r8d
	jle	.L21
	leal	-4(%rdi), %r10d
	leaq	24(%rdx), %rdi
	leaq	8(%rdx), %rax
	leaq	16(%rsi), %r11
	pushq	%rbx
	.cfi_def_cfa_offset 16
	.cfi_offset 3, -16
	leaq	28(%rsi), %rbx
	cmpq	%rdi, %rsi
	setae	%cl
	cmpq	%rax, %r11
	setbe	%r9b
	orl	%r9d, %ecx
	leaq	12(%rsi), %r9
	cmpq	%r9, %rdi
	setbe	%r9b
	cmpq	%rbx, %rax
	setae	%bl
	orl	%ebx, %r9d
	andl	%r9d, %ecx
	cmpl	$3, %r10d
	seta	%r9b
	andl	%r9d, %ecx
	cmpq	%r11, %rdi
	leaq	32(%rsi), %r11
	setbe	%r9b
	cmpq	%r11, %rax
	setae	%r11b
	orl	%r11d, %r9d
	leaq	24(%rsi), %r11
	andl	%r9d, %ecx
	leaq	8(%rsi), %r9
	cmpq	%r9, %rdi
	setbe	%r9b
	cmpq	%r11, %rax
	setae	%r11b
	orl	%r11d, %r9d
	testb	%r9b, %cl
	je	.L3
	leaq	4(%rsi), %rcx
	cmpq	%rcx, %rdi
	leaq	20(%rsi), %rcx
	setbe	%dil
	cmpq	%rcx, %rax
	setae	%cl
	orb	%cl, %dil
	je	.L3
	movl	%r10d, %r11d
	xorps	%xmm2, %xmm2
	shrl	$2, %r11d
	movaps	.LC0(%rip), %xmm4
	leal	0(,%r11,4), %r9d
	movq	%rsi, %rcx
	xorl	%edi, %edi
	movaps	.LC1(%rip), %xmm3
	movaps	.LC2(%rip), %xmm5
.L9:
	movaps	%xmm2, %xmm1
	movq	$0, (%rax)
	movq	$0, 8(%rax)
	movaps	%xmm2, %xmm0
	movlps	(%rcx), %xmm1
	addl	$1, %edi
	addq	$16, %rax
	addq	$16, %rcx
	movhps	-8(%rcx), %xmm1
	mulps	%xmm4, %xmm1
	addps	%xmm2, %xmm1
	movlps	%xmm1, -16(%rax)
	movhps	%xmm1, -8(%rax)
	movlps	-12(%rcx), %xmm0
	movhps	-4(%rcx), %xmm0
	mulps	%xmm3, %xmm0
	addps	%xmm1, %xmm0
	movaps	%xmm2, %xmm1
	movlps	%xmm0, -16(%rax)
	movhps	%xmm0, -8(%rax)
	movlps	-8(%rcx), %xmm1
	movhps	(%rcx), %xmm1
	mulps	%xmm5, %xmm1
	addps	%xmm0, %xmm1
	movaps	%xmm2, %xmm0
	movlps	%xmm1, -16(%rax)
	movhps	%xmm1, -8(%rax)
	movlps	-4(%rcx), %xmm0
	movhps	4(%rcx), %xmm0
	mulps	%xmm3, %xmm0
	addps	%xmm1, %xmm0
	movaps	%xmm2, %xmm1
	movlps	%xmm0, -16(%rax)
	movhps	%xmm0, -8(%rax)
	movlps	(%rcx), %xmm1
	movhps	8(%rcx), %xmm1
	mulps	%xmm4, %xmm1
	addps	%xmm0, %xmm1
	movlps	%xmm1, -16(%rax)
	movhps	%xmm1, -8(%rax)
	cmpl	%r11d, %edi
	jb	.L9
	cmpl	%r9d, %r10d
	leal	2(%r9), %eax
	je	.L1
	movslq	%eax, %r10
	xorps	%xmm2, %xmm2
	leaq	0(,%r10,4), %rcx
	movss	.LC4(%rip), %xmm0
	movss	.LC5(%rip), %xmm1
	leaq	(%rdx,%rcx), %rax
	movss	.LC6(%rip), %xmm5
	leaq	-8(%rcx), %rdi
	movss	%xmm2, (%rax)
	movss	-8(%rsi,%rcx), %xmm4
	mulss	%xmm0, %xmm4
	addss	%xmm2, %xmm4
	movss	%xmm4, (%rax)
	movss	-4(%rsi,%rcx), %xmm3
	leal	3(%r9), %ecx
	mulss	%xmm1, %xmm3
	cmpl	%ecx, %r8d
	addss	%xmm4, %xmm3
	movss	%xmm3, (%rax)
	movss	(%rsi,%r10,4), %xmm4
	movslq	%ecx, %r10
	mulss	%xmm5, %xmm4
	addss	%xmm3, %xmm4
	movss	%xmm4, (%rax)
	movss	12(%rsi,%rdi), %xmm3
	mulss	%xmm1, %xmm3
	addss	%xmm4, %xmm3
	movss	%xmm3, (%rax)
	movss	16(%rsi,%rdi), %xmm4
	mulss	%xmm0, %xmm4
	addss	%xmm3, %xmm4
	movss	%xmm4, (%rax)
	jle	.L1
	leaq	0(,%r10,4), %rcx
	addl	$4, %r9d
	cmpl	%r9d, %r8d
	leaq	(%rdx,%rcx), %rax
	leaq	-8(%rcx), %rdi
	movss	%xmm2, (%rax)
	movss	-8(%rsi,%rcx), %xmm4
	mulss	%xmm0, %xmm4
	addss	%xmm2, %xmm4
	movss	%xmm4, (%rax)
	movss	-4(%rsi,%rcx), %xmm3
	movslq	%r9d, %rcx
	mulss	%xmm1, %xmm3
	addss	%xmm4, %xmm3
	movss	%xmm3, (%rax)
	movss	(%rsi,%r10,4), %xmm4
	mulss	%xmm5, %xmm4
	addss	%xmm3, %xmm4
	movss	%xmm4, (%rax)
	movss	12(%rsi,%rdi), %xmm3
	mulss	%xmm1, %xmm3
	addss	%xmm4, %xmm3
	movss	%xmm3, (%rax)
	movss	16(%rsi,%rdi), %xmm4
	mulss	%xmm0, %xmm4
	addss	%xmm3, %xmm4
	movss	%xmm4, (%rax)
	jle	.L1
	leaq	0(,%rcx,4), %rax
	addq	%rax, %rdx
	movss	%xmm2, (%rdx)
	movss	-8(%rsi,%rax), %xmm4
	mulss	%xmm0, %xmm4
	addss	%xmm2, %xmm4
	movss	%xmm4, (%rdx)
	movss	-4(%rsi,%rax), %xmm3
	mulss	%xmm1, %xmm3
	addss	%xmm4, %xmm3
	movss	%xmm3, (%rdx)
	movss	(%rsi,%rcx,4), %xmm2
	mulss	%xmm5, %xmm2
	addss	%xmm3, %xmm2
	movss	%xmm2, (%rdx)
	mulss	4(%rsi,%rax), %xmm1
	addss	%xmm2, %xmm1
	movss	%xmm1, (%rdx)
	mulss	8(%rsi,%rax), %xmm0
	addss	%xmm1, %xmm0
	movss	%xmm0, (%rdx)
.L1:
	popq	%rbx
	.cfi_restore 3
	.cfi_def_cfa_offset 8
.L21:
	rep ret
	.p2align 4,,10
	.p2align 3
.L3:
	.cfi_def_cfa_offset 16
	.cfi_offset 3, -16
	xorps	%xmm5, %xmm5
	movl	$2, %edx
	movss	.LC4(%rip), %xmm3
	movss	.LC5(%rip), %xmm2
	movss	.LC6(%rip), %xmm4
	.p2align 4,,10
	.p2align 3
.L11:
	movl	$0x00000000, (%rax)
	addl	$1, %edx
	addq	$4, %rax
	movss	(%rsi), %xmm1
	addq	$4, %rsi
	mulss	%xmm3, %xmm1
	addss	%xmm5, %xmm1
	movss	%xmm1, -4(%rax)
	movss	(%rsi), %xmm0
	mulss	%xmm2, %xmm0
	addss	%xmm1, %xmm0
	movss	%xmm0, -4(%rax)
	movss	4(%rsi), %xmm1
	mulss	%xmm4, %xmm1
	addss	%xmm0, %xmm1
	movss	%xmm1, -4(%rax)
	movss	8(%rsi), %xmm0
	mulss	%xmm2, %xmm0
	addss	%xmm1, %xmm0
	movss	%xmm0, -4(%rax)
	movss	12(%rsi), %xmm1
	mulss	%xmm3, %xmm1
	addss	%xmm0, %xmm1
	movss	%xmm1, -4(%rax)
	cmpl	%edx, %r8d
	jne	.L11
	popq	%rbx
	.cfi_restore 3
	.cfi_def_cfa_offset 8
	jmp	.L21
	.cfi_endproc
.LFE0:
	.size	conv, .-conv
	.section	.rodata.cst16,"aM",@progbits,16
	.align 16
.LC0:
	.long	1036831949
	.long	1036831949
	.long	1036831949
	.long	1036831949
	.align 16
.LC1:
	.long	1048576000
	.long	1048576000
	.long	1048576000
	.long	1048576000
	.align 16
.LC2:
	.long	1050253722
	.long	1050253722
	.long	1050253722
	.long	1050253722
	.section	.rodata.cst4,"aM",@progbits,4
	.align 4
.LC4:
	.long	1036831949
	.align 4
.LC5:
	.long	1048576000
	.align 4
.LC6:
	.long	1050253722
	.ident	"GCC: (Ubuntu 4.8.2-19ubuntu1) 4.8.2"
	.section	.note.GNU-stack,"",@progbits
