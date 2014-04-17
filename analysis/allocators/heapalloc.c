#include <stdlib.h>
#include <stdio.h>

#define alloc_pair(n) { \
        char *a = malloc(n); \
        char *b = malloc(n); \
        printf("%d,%p,%p\n", n, a, b); \
    }

int main(int argc, char* argv[])
{
    alloc_pair(64)
    alloc_pair(1024)
    alloc_pair(5120)
    alloc_pair(1 << 20) // 1 048 576
    return 0;
}
