#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>

static void write_null(void) {
    int storage = 0;
    int *destination = &storage;
    printf("destination: %p\n", (void *)destination);
    *destination = 42;
}

static void overwrite_neighbor(void) {
    struct { int items[4]; int boundary; } block = {{0}, 100};
    printf("boundary before: %d\n", block.boundary);
    for (int cursor = 0; cursor < 4; ++cursor)
        block.items[cursor] = 7;
    printf("boundary after: %d\n", block.boundary);
}

static void overwrite_heap(void) {
    int *values = malloc(4 * sizeof *values);
    if (!values) exit(2);
    int cursor;
    for (cursor = 0; cursor < 4; ++cursor)
        values[cursor] = 7;
    printf("stored %d values; allocated space for 4\n", cursor);
    free(values);
}

static void read_released(void) {
    char *label = malloc(16);
    if (!label) exit(2);
    strcpy(label, "probe");
    printf("valid label: %s\n", label);
    free(label);
}

int main(int argument_count, char **arguments) {
    SetErrorMode(SEM_FAILCRITICALERRORS | SEM_NOGPFAULTERRORBOX);
    setvbuf(stdout, NULL, _IONBF, 0);
    const char *scenario = argument_count > 1 ? arguments[1] : "";
    if (!strcmp(scenario, "null")) write_null();
    else if (!strcmp(scenario, "overflow")) overwrite_neighbor();
    else if (!strcmp(scenario, "heap")) overwrite_heap();
    else if (!strcmp(scenario, "uaf")) read_released();
    else return 1;
    return 0;
}
