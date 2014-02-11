
test:     file format elf64-x86-64


Disassembly of section .init:

00000000004003e0 <_init>:
  4003e0:	48 83 ec 08          	sub    $0x8,%rsp
  4003e4:	48 8b 05 0d 0c 20 00 	mov    0x200c0d(%rip),%rax        # 600ff8 <_DYNAMIC+0x1d0>
  4003eb:	48 85 c0             	test   %rax,%rax
  4003ee:	74 05                	je     4003f5 <_init+0x15>
  4003f0:	e8 3b 00 00 00       	callq  400430 <__gmon_start__@plt>
  4003f5:	48 83 c4 08          	add    $0x8,%rsp
  4003f9:	c3                   	retq   

Disassembly of section .plt:

0000000000400400 <printf@plt-0x10>:
  400400:	ff 35 02 0c 20 00    	pushq  0x200c02(%rip)        # 601008 <_GLOBAL_OFFSET_TABLE_+0x8>
  400406:	ff 25 04 0c 20 00    	jmpq   *0x200c04(%rip)        # 601010 <_GLOBAL_OFFSET_TABLE_+0x10>
  40040c:	0f 1f 40 00          	nopl   0x0(%rax)

0000000000400410 <printf@plt>:
  400410:	ff 25 02 0c 20 00    	jmpq   *0x200c02(%rip)        # 601018 <_GLOBAL_OFFSET_TABLE_+0x18>
  400416:	68 00 00 00 00       	pushq  $0x0
  40041b:	e9 e0 ff ff ff       	jmpq   400400 <_init+0x20>

0000000000400420 <__libc_start_main@plt>:
  400420:	ff 25 fa 0b 20 00    	jmpq   *0x200bfa(%rip)        # 601020 <_GLOBAL_OFFSET_TABLE_+0x20>
  400426:	68 01 00 00 00       	pushq  $0x1
  40042b:	e9 d0 ff ff ff       	jmpq   400400 <_init+0x20>

0000000000400430 <__gmon_start__@plt>:
  400430:	ff 25 f2 0b 20 00    	jmpq   *0x200bf2(%rip)        # 601028 <_GLOBAL_OFFSET_TABLE_+0x28>
  400436:	68 02 00 00 00       	pushq  $0x2
  40043b:	e9 c0 ff ff ff       	jmpq   400400 <_init+0x20>

Disassembly of section .text:

0000000000400440 <_start>:
  400440:	31 ed                	xor    %ebp,%ebp
  400442:	49 89 d1             	mov    %rdx,%r9
  400445:	5e                   	pop    %rsi
  400446:	48 89 e2             	mov    %rsp,%rdx
  400449:	48 83 e4 f0          	and    $0xfffffffffffffff0,%rsp
  40044d:	50                   	push   %rax
  40044e:	54                   	push   %rsp
  40044f:	49 c7 c0 70 06 40 00 	mov    $0x400670,%r8
  400456:	48 c7 c1 e0 05 40 00 	mov    $0x4005e0,%rcx
  40045d:	48 c7 c7 2d 05 40 00 	mov    $0x40052d,%rdi
  400464:	e8 b7 ff ff ff       	callq  400420 <__libc_start_main@plt>
  400469:	f4                   	hlt    
  40046a:	66 0f 1f 44 00 00    	nopw   0x0(%rax,%rax,1)

0000000000400470 <deregister_tm_clones>:
  400470:	b8 47 10 60 00       	mov    $0x601047,%eax
  400475:	55                   	push   %rbp
  400476:	48 2d 40 10 60 00    	sub    $0x601040,%rax
  40047c:	48 83 f8 0e          	cmp    $0xe,%rax
  400480:	48 89 e5             	mov    %rsp,%rbp
  400483:	77 02                	ja     400487 <deregister_tm_clones+0x17>
  400485:	5d                   	pop    %rbp
  400486:	c3                   	retq   
  400487:	b8 00 00 00 00       	mov    $0x0,%eax
  40048c:	48 85 c0             	test   %rax,%rax
  40048f:	74 f4                	je     400485 <deregister_tm_clones+0x15>
  400491:	5d                   	pop    %rbp
  400492:	bf 40 10 60 00       	mov    $0x601040,%edi
  400497:	ff e0                	jmpq   *%rax
  400499:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)

00000000004004a0 <register_tm_clones>:
  4004a0:	b8 40 10 60 00       	mov    $0x601040,%eax
  4004a5:	55                   	push   %rbp
  4004a6:	48 2d 40 10 60 00    	sub    $0x601040,%rax
  4004ac:	48 c1 f8 03          	sar    $0x3,%rax
  4004b0:	48 89 e5             	mov    %rsp,%rbp
  4004b3:	48 89 c2             	mov    %rax,%rdx
  4004b6:	48 c1 ea 3f          	shr    $0x3f,%rdx
  4004ba:	48 01 d0             	add    %rdx,%rax
  4004bd:	48 d1 f8             	sar    %rax
  4004c0:	75 02                	jne    4004c4 <register_tm_clones+0x24>
  4004c2:	5d                   	pop    %rbp
  4004c3:	c3                   	retq   
  4004c4:	ba 00 00 00 00       	mov    $0x0,%edx
  4004c9:	48 85 d2             	test   %rdx,%rdx
  4004cc:	74 f4                	je     4004c2 <register_tm_clones+0x22>
  4004ce:	5d                   	pop    %rbp
  4004cf:	48 89 c6             	mov    %rax,%rsi
  4004d2:	bf 40 10 60 00       	mov    $0x601040,%edi
  4004d7:	ff e2                	jmpq   *%rdx
  4004d9:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)

00000000004004e0 <__do_global_dtors_aux>:
  4004e0:	80 3d 59 0b 20 00 00 	cmpb   $0x0,0x200b59(%rip)        # 601040 <__TMC_END__>
  4004e7:	75 11                	jne    4004fa <__do_global_dtors_aux+0x1a>
  4004e9:	55                   	push   %rbp
  4004ea:	48 89 e5             	mov    %rsp,%rbp
  4004ed:	e8 7e ff ff ff       	callq  400470 <deregister_tm_clones>
  4004f2:	5d                   	pop    %rbp
  4004f3:	c6 05 46 0b 20 00 01 	movb   $0x1,0x200b46(%rip)        # 601040 <__TMC_END__>
  4004fa:	f3 c3                	repz retq 
  4004fc:	0f 1f 40 00          	nopl   0x0(%rax)

0000000000400500 <frame_dummy>:
  400500:	48 83 3d 18 09 20 00 	cmpq   $0x0,0x200918(%rip)        # 600e20 <__JCR_END__>
  400507:	00 
  400508:	74 1e                	je     400528 <frame_dummy+0x28>
  40050a:	b8 00 00 00 00       	mov    $0x0,%eax
  40050f:	48 85 c0             	test   %rax,%rax
  400512:	74 14                	je     400528 <frame_dummy+0x28>
  400514:	55                   	push   %rbp
  400515:	bf 20 0e 60 00       	mov    $0x600e20,%edi
  40051a:	48 89 e5             	mov    %rsp,%rbp
  40051d:	ff d0                	callq  *%rax
  40051f:	5d                   	pop    %rbp
  400520:	e9 7b ff ff ff       	jmpq   4004a0 <register_tm_clones>
  400525:	0f 1f 00             	nopl   (%rax)
  400528:	e9 73 ff ff ff       	jmpq   4004a0 <register_tm_clones>

000000000040052d <main>:
  40052d:	55                   	push   %rbp
  40052e:	48 89 e5             	mov    %rsp,%rbp
  400531:	48 83 ec 10          	sub    $0x10,%rsp
  400535:	c7 45 f8 00 00 00 00 	movl   $0x0,-0x8(%rbp)
  40053c:	c7 45 fc 01 00 00 00 	movl   $0x1,-0x4(%rbp)
  400543:	eb 3c                	jmp    400581 <main+0x54>
  400545:	8b 15 f9 0a 20 00    	mov    0x200af9(%rip),%edx        # 601044 <i>
  40054b:	8b 45 fc             	mov    -0x4(%rbp),%eax
  40054e:	01 d0                	add    %edx,%eax
  400550:	89 05 ee 0a 20 00    	mov    %eax,0x200aee(%rip)        # 601044 <i>
  400556:	8b 15 ec 0a 20 00    	mov    0x200aec(%rip),%edx        # 601048 <j>
  40055c:	8b 45 fc             	mov    -0x4(%rbp),%eax
  40055f:	01 d0                	add    %edx,%eax
  400561:	89 05 e1 0a 20 00    	mov    %eax,0x200ae1(%rip)        # 601048 <j>
  400567:	8b 15 df 0a 20 00    	mov    0x200adf(%rip),%edx        # 60104c <k>
  40056d:	8b 45 fc             	mov    -0x4(%rbp),%eax
  400570:	01 d0                	add    %edx,%eax
  400572:	89 05 d4 0a 20 00    	mov    %eax,0x200ad4(%rip)        # 60104c <k>
  400578:	8b 45 f8             	mov    -0x8(%rbp),%eax
  40057b:	83 c0 01             	add    $0x1,%eax
  40057e:	89 45 f8             	mov    %eax,-0x8(%rbp)
  400581:	8b 45 f8             	mov    -0x8(%rbp),%eax
  400584:	3d ff ff 00 00       	cmp    $0xffff,%eax
  400589:	7e ba                	jle    400545 <main+0x18>
  40058b:	48 8d 55 fc          	lea    -0x4(%rbp),%rdx
  40058f:	48 8d 45 f8          	lea    -0x8(%rbp),%rax
  400593:	48 89 d6             	mov    %rdx,%rsi
  400596:	48 89 c7             	mov    %rax,%rdi
  400599:	e8 07 00 00 00       	callq  4005a5 <output>
  40059e:	b8 00 00 00 00       	mov    $0x0,%eax
  4005a3:	c9                   	leaveq 
  4005a4:	c3                   	retq   

00000000004005a5 <output>:
  4005a5:	55                   	push   %rbp
  4005a6:	48 89 e5             	mov    %rsp,%rbp
  4005a9:	48 83 ec 10          	sub    $0x10,%rsp
  4005ad:	48 89 7d f8          	mov    %rdi,-0x8(%rbp)
  4005b1:	48 89 75 f0          	mov    %rsi,-0x10(%rbp)
  4005b5:	48 8d 55 f0          	lea    -0x10(%rbp),%rdx
  4005b9:	48 8d 45 f8          	lea    -0x8(%rbp),%rax
  4005bd:	48 89 c6             	mov    %rax,%rsi
  4005c0:	bf 84 06 40 00       	mov    $0x400684,%edi
  4005c5:	b8 00 00 00 00       	mov    $0x0,%eax
  4005ca:	e8 41 fe ff ff       	callq  400410 <printf@plt>
  4005cf:	c9                   	leaveq 
  4005d0:	c3                   	retq   
  4005d1:	66 2e 0f 1f 84 00 00 	nopw   %cs:0x0(%rax,%rax,1)
  4005d8:	00 00 00 
  4005db:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)

00000000004005e0 <__libc_csu_init>:
  4005e0:	48 89 6c 24 d8       	mov    %rbp,-0x28(%rsp)
  4005e5:	4c 89 64 24 e0       	mov    %r12,-0x20(%rsp)
  4005ea:	48 8d 2d 27 08 20 00 	lea    0x200827(%rip),%rbp        # 600e18 <__init_array_end>
  4005f1:	4c 8d 25 18 08 20 00 	lea    0x200818(%rip),%r12        # 600e10 <__frame_dummy_init_array_entry>
  4005f8:	48 89 5c 24 d0       	mov    %rbx,-0x30(%rsp)
  4005fd:	4c 89 6c 24 e8       	mov    %r13,-0x18(%rsp)
  400602:	4c 89 74 24 f0       	mov    %r14,-0x10(%rsp)
  400607:	4c 89 7c 24 f8       	mov    %r15,-0x8(%rsp)
  40060c:	48 83 ec 38          	sub    $0x38,%rsp
  400610:	4c 29 e5             	sub    %r12,%rbp
  400613:	41 89 ff             	mov    %edi,%r15d
  400616:	49 89 f6             	mov    %rsi,%r14
  400619:	48 c1 fd 03          	sar    $0x3,%rbp
  40061d:	49 89 d5             	mov    %rdx,%r13
  400620:	31 db                	xor    %ebx,%ebx
  400622:	e8 b9 fd ff ff       	callq  4003e0 <_init>
  400627:	48 85 ed             	test   %rbp,%rbp
  40062a:	74 1a                	je     400646 <__libc_csu_init+0x66>
  40062c:	0f 1f 40 00          	nopl   0x0(%rax)
  400630:	4c 89 ea             	mov    %r13,%rdx
  400633:	4c 89 f6             	mov    %r14,%rsi
  400636:	44 89 ff             	mov    %r15d,%edi
  400639:	41 ff 14 dc          	callq  *(%r12,%rbx,8)
  40063d:	48 83 c3 01          	add    $0x1,%rbx
  400641:	48 39 eb             	cmp    %rbp,%rbx
  400644:	75 ea                	jne    400630 <__libc_csu_init+0x50>
  400646:	48 8b 5c 24 08       	mov    0x8(%rsp),%rbx
  40064b:	48 8b 6c 24 10       	mov    0x10(%rsp),%rbp
  400650:	4c 8b 64 24 18       	mov    0x18(%rsp),%r12
  400655:	4c 8b 6c 24 20       	mov    0x20(%rsp),%r13
  40065a:	4c 8b 74 24 28       	mov    0x28(%rsp),%r14
  40065f:	4c 8b 7c 24 30       	mov    0x30(%rsp),%r15
  400664:	48 83 c4 38          	add    $0x38,%rsp
  400668:	c3                   	retq   
  400669:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)

0000000000400670 <__libc_csu_fini>:
  400670:	f3 c3                	repz retq 

Disassembly of section .fini:

0000000000400674 <_fini>:
  400674:	48 83 ec 08          	sub    $0x8,%rsp
  400678:	48 83 c4 08          	add    $0x8,%rsp
  40067c:	c3                   	retq   
