#include <stdlib.h>
#include <stdio.h>

#define N 0x100000
// static float kernel[5] = {0.1, 0.25, 0.3, 0.25, 0.1};

// void convolve(int size, float *input, float *output)
// {
//     int i, j;
//     for (i = 2; i < size - 2; ++i)
//     {
//         output[i] = 0;
//         for (j = 0; j < 5; ++j)
//             output[i] += input[i-2+j] * kernel[j];
//     }
// }

void convolve(int, float *, float *);

int main(int argc, char **argv)
{
    // Needed for automated test script
    int repeat = argc > 1 ? atoi(argv[1]) : 0; // Repeat function invocation
    int offset = argc > 2 ? atoi(argv[2]) : 0; // Offset between buffers
    int i;

    float *input  = malloc( N          * sizeof(float));
    float *output = malloc((N + 0x100) * sizeof(float));

    // To make a realistic test, initialize the otherwise all-zero input array
    for (srand(0), i = 0; i < N; ++i) {
        input[i] = (float)rand();
    }

    // Repeat a variable number of times, to be able to subtract the 
    // constant overhead from allocating and initializing input arrays.
    for (i = 0; i < repeat; ++i) {
        convolve(N, input, (output + offset));
    }

    //printf("Offset: %d : (%p, %p), repeat %d\n", offset, input, output, repeat);

    return 0;
}
