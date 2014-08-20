#include <stdlib.h>
#include <stdio.h>
#include <cblas.h>
#include <sys/mman.h>

// M rows x N cols
#define M 1024
#define N 1024

#define ALIGNED_ALLOC(n) \
    ((char*) mmap(NULL, n, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0))

int main(int argc, char **argv) {
    int n  = argc > 1 ? atoi(argv[1]) : 1;
    int dx = argc > 2 ? 16 * atoi(argv[2]) : 0;
    int dy = argc > 3 ? 16 * atoi(argv[3]) : 0;
    int i;

    // Matrix-vector multiplication, y = alpha*Ax + beta*y
    const double alpha = 1.0, beta = 0.0;

    double *A, *x, *y;

    // Ensure page alignment as baseline. Keep matrix A at offset 0x000 even though
    // for libc allocator it will by default always be 0x010. Easiest way to 
    // achieve this is probably mmap, so might as well use that.
    A = (double*) ALIGNED_ALLOC(M*N*sizeof(double));
    x = (double*) (ALIGNED_ALLOC(N*sizeof(double)+4096) + dx);
    y = (double*) (ALIGNED_ALLOC(M*sizeof(double)+4096) + dy);

    // Aliasing effects are slightly more visible for sparse (or zero) matrices, 
    // resulting in fewer operations overall, while the number of alias events is 
    // constant. Also keeps the example simple.
    for (i = 0; i < N; ++i) {
        A[i*N + i] = 1; 
        x[i] = i;
    }

    // Repeat invocation to filter out constant overhead from allocation and
    // initialization.
    for (i = 0; i < n; ++i)
        cblas_dgemv(
            CblasColMajor, 
            CblasNoTrans,
            M, N,
            alpha, 
            A, M,
            x, 1, 
            beta, 
            y, 1
        );

    // printf("A:%p x:%p y:%p\n", A, x, y);
    return 0;
}
