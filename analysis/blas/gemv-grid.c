#include <stdlib.h>
#include <stdio.h>
#include <cblas.h>
#include <sys/mman.h>

// M rows x N cols
#define M 256
#define N 256

#define ALIGNED_ALLOC(n) \
    ((char*) mmap(NULL, n, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0))

int main(int argc, char **argv) {
    int dx = argc > 1 ? atoi(argv[1]) : 0;
    int dy = argc > 2 ? atoi(argv[2]) : 0;
    int n  = argc > 3 ? atoi(argv[3]) : 1;
    int i;

    // Matrix-vector multiplication, y = alpha*Ax + beta*y
    const double alpha = 1.0, beta = 0.0;

    double *A, *x, *y;

    // Ensure page alignment as baseline. Keep matrix A at offset 0x000 even though
    // for libc allocator it will by default always be 0x010. Have not observed any
    // side effects of this.

    // Easiest way to achieve this is probably mmap, so will just use that
    A = (double*) ALIGNED_ALLOC(M*N*sizeof(double));
    x = (double*) (ALIGNED_ALLOC(N*sizeof(double)+4096) + dx);
    y = (double*) (ALIGNED_ALLOC(M*sizeof(double)+4096) + dy);

    // TODO: Check if use of aligned_alloc is actually sane, not mmaped?
    //A = (double*) (aligned_alloc(4096, (M*N*sizeof(double)+4096) & -4096) + 0);
    // Allocate an extra page for possible offset of x and y vectors
    //x = (double*) (aligned_alloc(4096, (N*sizeof(double)+4096*2) & -4096) + dx);
    //y = (double*) (aligned_alloc(4096, (M*sizeof(double)+4096*2) & -4096) + dy);

    srand(0);

    for (i = 0; i < M*N; ++i) A[i] = (double) rand();
    for (i = 0; i < N; ++i) x[i] = (double) rand();

    for (i = 0; i < n; ++i)
        cblas_dgemv(CblasColMajor, 
            CblasNoTrans, // Transpose A
            M, N, // rows, cols
            alpha, 
            A, M, // lda (offset to next column with same row index)
            x, 1, 
            beta, 
            y, 1
        );

    //printf("A:%p x:%p y:%p\n", A, x, y);
    return 0;
}
