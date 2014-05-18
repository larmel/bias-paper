	.file	"loop.c"
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
	jmp	.L2
.L3:
	movl	i(%rip), %edx 	# load i
	movl	-4(%rbp), %eax 	# load inc
	addl	%edx, %eax
	movl	%eax, i(%rip)   # store i
	movl	j(%rip), %edx
	movl	-4(%rbp), %eax  # load inc
	addl	%edx, %eax
	movl	%eax, j(%rip)
	movl	k(%rip), %edx
	movl	-4(%rbp), %eax  # load inc
	addl	%edx, %eax
	movl	%eax, k(%rip)
	addl	$1, -8(%rbp)
.L2:
	cmpl	$65535, -8(%rbp)
	jle	.L3
	movl	$0, %eax
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.size	main, .-main
	.ident	"GCC: (Ubuntu 4.8.2-19ubuntu1) 4.8.2"
	.section	.note.GNU-stack,"",@progbits
