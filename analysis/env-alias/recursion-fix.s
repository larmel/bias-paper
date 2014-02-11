	.file	"recursion-fix.c"
	.local	i
	.comm	i,4,4
	.local	j
	.comm	j,4,4
	.local	k
	.comm	k,4,4
	.text
	.globl	main
	.type	main, @function
main:
.LFB0:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movl	$0, -8(%rbp)
	movl	$1, -4(%rbp)
	leaq	-4(%rbp), %rdx
	movl	$i, %eax
	xorq	%rdx, %rax
	andl	$4095, %eax
	testq	%rax, %rax
	je	.L2
	leaq	-8(%rbp), %rdx
	movl	$i, %eax
	xorq	%rdx, %rax
	andl	$4095, %eax
	testq	%rax, %rax
	jne	.L3
.L2:
	movl	$0, %eax
	jmp	.L7
.L3:
	jmp	.L5
.L6:
	movl	i(%rip), %edx
	movl	-4(%rbp), %eax
	addl	%edx, %eax
	movl	%eax, i(%rip)
	movl	j(%rip), %edx
	movl	-4(%rbp), %eax
	addl	%edx, %eax
	movl	%eax, j(%rip)
	movl	k(%rip), %edx
	movl	-4(%rbp), %eax
	addl	%edx, %eax
	movl	%eax, k(%rip)
	movl	-8(%rbp), %eax
	addl	$1, %eax
	movl	%eax, -8(%rbp)
.L5:
	movl	-8(%rbp), %eax
	cmpl	$655359, %eax
	jle	.L6
	movl	$0, %eax
.L7:
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.size	main, .-main
	.ident	"GCC: (Ubuntu/Linaro 4.8.1-10ubuntu9) 4.8.1"
	.section	.note.GNU-stack,"",@progbits
