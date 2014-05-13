static float kernel[5] = {0.1, 0.25, 0.3, 0.25, 0.1};

void convolve(int size, const float *input, float *output)
{
    int i, j;
    for (i = 2; i < size - 2; ++i)
    {
        output[i] = 0;
        for (j = 0; j < 5; ++j)
            output[i] += input[i-2+j] * kernel[j];
    }
}
