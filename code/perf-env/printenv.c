/// Program that prints its own environment, illustrates how running perf-stat
/// adds some environment variables.
///
/// $ perf stat env -i ./printenv
///     <empty>
///
/// $ env -i perf stat ./printenv
///	    PWD=/home/lars/bias-paper/code/perf-env
///     SHLVL=0
///     PERF_BUILDID_DIR=.debug
///     PATH=/usr/libexec/perf-core:/usr/lib/linux-tools/3.11.0-15-generic:/usr/local/bin:/usr/bin:/bin
///
/// $ perf stat ./printenv
///	    PWD=/home/lars/bias-paper/code/perf-env
///     SHLVL=0
///     PERF_BUILDID_DIR=.debug
///     PATH=/usr/libexec/perf-core:/usr/lib/linux-tools/3.11.0-15-generic:/usr/local/bin:/usr/bin:/bin
///     (+ whatever was already there)
///
#include <stdio.h>
#include <string.h>

int main() {
	char file[64], command[128];
	sprintf(file, "/proc/%d/environ", getpid());

	strcpy(command, "cat ");
	strcat(command, file);
	system(command);

	putchar('\n');

	strcat(command, " | wc -c");
	system(command);

	printf("stack: %p\n", (void*)file);

	return 0;
}
