#include <stdlib.h>
#include <stdio.h>

int main(int argc, char* argv[])
{
	if (argc < 2)
		return 1;
	int size = atoi(argv[1]);

	char *a = malloc(size);	
	char *b = malloc(size);

	printf("%p %p", a, b);
    return 0;
}
