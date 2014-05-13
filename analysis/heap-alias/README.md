Used in paper

    make bin/default-o3.1.csv
    make bin/default-o3.11.csv
    make bin/default-o3.estimate.csv

Also interesting (very clean bias graph)

    make bin/default-o2.1.csv
    make bin/default-o2.11.csv
    make bin/default-o2.estimate.csv

Code generated with -O3 is heavily vectorized with GCC. Adding -march=native significantly reduces
aliasing, but still not perfect performance for default alignment.
