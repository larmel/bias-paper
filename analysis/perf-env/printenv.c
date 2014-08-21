/// Program that prints its own environment, illustrates how running perf-stat
/// adds some environment variables.
///
/// $ perf stat env -i ./printenv
///     <empty>
///
/// $ env -i perf stat ./printenv
///     PWD=/home/lars/bias-paper/code/perf-env
///     SHLVL=0
///     PERF_BUILDID_DIR=.debug
///     PATH=/usr/libexec/perf-core:/usr/lib/linux-tools/3.11.0-15-generic:/usr/local/bin:/usr/bin:/bin
///
/// $ perf stat ./printenv
///     PWD=/home/lars/bias-paper/code/perf-env
///     SHLVL=0
///     PERF_BUILDID_DIR=.debug
///     PATH=/usr/libexec/perf-core:/usr/lib/linux-tools/3.11.0-15-generic:/usr/local/bin:/usr/bin:/bin
///     (+ whatever was already there)
///
#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
    long i = 0, *addr;
    char file[64], command[128];

    for (; i < argc; ++i) 
        puts(argv[i]);
    puts("");

    sprintf(file, "/proc/%d/environ", getpid());

    strcpy(command, "cat ");
    strcat(command, file);
    system(command);

    puts("");

    strcat(command, " | wc -c");
    system(command);

    asm("movq %%rbp, %0" : "=r"(addr));
    printf("%%rbp: %p\n", (void*)&addr);

    return 0;
}
