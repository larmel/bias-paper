#include <stdlib.h>
#include <stdio.h>
#include <cblas.h>

// A is M rows x N cols
#define M 8192
#define N 8192

int main(int argc, char **argv) {
    int offset1 = argc > 1 ? atoi(argv[1]) : 0;
    int offset2 = argc > 2 ? atoi(argv[2]) : 0;
    int iters   = argc > 3 ? atoi(argv[3]) : 1;

    // Matrix-vector multiplication, y = alpha*Ax + beta*y
    const double alpha = 1.0, beta = 0.0;
    double *A, *x, *y;

    // Ensure random numbers are deterministic. Fill matrix A and input vector
    // x with non-zero values for a more realistic test scenario. However,
    // the cycle count is significantly reduced by using zero input, reinforcing
    // aliasing effects.
    srand(0);

    // The matrix is big and will be mmap allocated.
    A = malloc(sizeof(double) * M * N);
    for (int i = 0; i < M * N; A[i++] = (double) rand())
        ;

    // Offset to manipulate normal heap addresses.
    if (offset1) malloc(offset1);

    // x and y are small and willb e allocated on normal heap.
    x = malloc(sizeof(double) * N);
    for (int i = 0; i < N; x[i++] = (double) rand())
        ;

    // Offset to separate x and y addresses.
    if (offset2) malloc(offset2);

    y = malloc(sizeof(double) * M);

    for (int i = 0; i < iters; ++i)
        cblas_dgemv(CblasColMajor, 
            CblasNoTrans, // Transpose A
            M, N,         // rows, cols
            alpha, 
            A, M,         // lda (offset to next column with same row index)
            x, 1, 
            beta, 
            y, 1
        );

    printf("A:%p x:%p y:%p\n", A, x, y);
    return 0;
}
