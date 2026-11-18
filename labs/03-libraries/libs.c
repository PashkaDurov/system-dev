#include <math.h>
#include <stdio.h>

int main(int argument_count, char *arguments[]) {
    double radicand = argument_count + 1.0;
    printf("%s: sqrt(%.0f) = %f\n", arguments[0], radicand, sqrt(radicand));
    return 0;
}
