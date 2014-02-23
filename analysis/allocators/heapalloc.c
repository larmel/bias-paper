#include <stdlib.h>
#include <stdio.h>

#define alloc_pair(n) { \
        float *a = malloc(n); \
        float *b = malloc(n); \
        printf("%d,%p,%p\n", n, a, b); \
    }

int main(void) {
    alloc_pair(64)
    alloc_pair(1024)
    alloc_pair(3001)
    alloc_pair(4096)

    alloc_pair(5111)
    alloc_pair(8192)
    alloc_pair(20000)
    alloc_pair(100000)
    alloc_pair(1 << 20) // 1 048 576
    alloc_pair(1 << 22)
    alloc_pair(1 << 24)
    alloc_pair(1 << 28)
    alloc_pair(1 << 30) // 1 GiB
    return 0;
}
