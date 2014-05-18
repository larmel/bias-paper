static float k[5] = {0.1, 0.25, 0.3, 0.25, 0.1};

void conv(int n, const float *input, float *output)
{
    int i, j;
    for (i = 2; i < n - 2; ++i)
    {
        output[i] = 0;
        for (j = 0; j < 5; ++j)
            output[i] += input[i-2+j] * k[j];
    }
}
