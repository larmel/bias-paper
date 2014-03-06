#include <stdlib.h>
#include <stdio.h>
#include <cblas.h>

#define M 64
#define N 64

int main(int argc, char **argv) {
    int dx = argc > 1 ? atoi(argv[1]) : 0;
    int dy = argc > 2 ? atoi(argv[2]) : 0;
    int n  = argc > 3 ? atoi(argv[3]) : 1;
    int i;

    // Matrix-vector multiplication, y = alpha*Ax + beta*y
    const double alpha = 1.0, beta = 0.0;
    double *A, *x, *y;

    // Ensure all buffers are page aligned, offset in number of bytes.
    A = (double*) aligned_alloc(0x1000, 0x10000);
    x = (double*) (aligned_alloc(0x1000, 0x2000) + dx);
    y = (double*) (aligned_alloc(0x1000, 0x2000) + dy);

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
