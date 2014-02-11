#include <stdio.h>

static int i, j, k;

static char* str = "%p, %p\n";

void output(void* a, void* b);

int main() {
    int g = 0, inc = 1;

    for (; g < 65536; g++) {
        i += inc;
        j += inc;
        k += inc;
    }
    output(&g, &inc);
/*
    asm __volatile__ (
    	"mov $1 %0\n"
    	""
    	:
    	: "r"(g), "r"(inc)
    	: );
*/
    return 0;
}

void output(void* a, void* b) {
    printf(str, a, b);
}
