static float k[5]= {0.1, 0.25, 0.3, 0.25, 0.1};
void conv(int n, const float *in, float *out) {
    for (int i = 2; i < n - 2; ++i) {
        out[i] = 0;
        for (int j = 0; j < 5; ++j)
            out[i] += in[i-2+j] * k[j];
    }
}
