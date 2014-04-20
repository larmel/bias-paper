#include <stdlib.h>
#include <stdio.h>
#include <cblas.h>
#include <sys/mman.h>

// void cblas_daxpy (const int N, const double alpha, const double *X, const int incX, double *Y, const int incY);

#define N (1 << 10)
#define T float
#define axpy cblas_saxpy

#define ALIGNED_ALLOC(n) \
    ((char*) mmap(NULL, n, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0))

int main(int argc, char **argv) {
    int n  = argc > 1 ? atoi(argv[1]) : 1;
    int dx = argc > 2 ? atoi(argv[2]) : 0;
    int i;

    // y = alpha x + y
    const T alpha = 1.0;

    // Make y page aligned, offset x from page alignment
    T *y = (T*) ALIGNED_ALLOC(N*sizeof(T));
    T *x = (T*) (ALIGNED_ALLOC(N*sizeof(T) + 4096)) + dx;

    srand(0);

    // Initialize separately to not introduce additional alias
    for (i = 0; i < N; ++i) y[i] = (T) rand();
    for (i = 0; i < N; ++i) x[i] = (T) rand();

    for (i = 0; i < n; ++i)
        axpy(N, alpha, x, 1, y, 1);

    //printf("x:%p y:%p\n", x, y);
    return 0;
}
