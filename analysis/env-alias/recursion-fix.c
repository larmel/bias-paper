#define ALIAS(a, b) \
    ((((long)&a)&0xfff)==(((long)&b)&0xfff))

static int i, j, k;

int main() {
    int g = 0, inc = 1;

    // Analyzing run-time addresses of automatic variables g and inc revealed
    // that worst case performance happens when i alias with inc.
    // Offset by another call frame in case of alias. Note that which 
    // variables alias is compiler-dependent. For a different static allocation
    // of i, j, k, this case could be impossible due to alignment guarantees,
    // but instead there would be another pair of aliasing variables. For
    // the same case in thesis "Analyzing Contextual Bias of Program
    // Execution on Modern CPUs", we found that inc alias with j.
    // Plot twist: The order inc and g is allocated on stack depends on the check
    // performed here, causing this approach to fail when only checking one
    // pair for collision => the other pair will collide instead.
    if (ALIAS(inc, i) || ALIAS(g, i))
        return main();

    for (; g < 65536; g++) {
        i += inc;
        j += inc;
        k += inc;
    }

    return 0;
}
