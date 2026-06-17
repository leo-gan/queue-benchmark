#ifndef DATA_LOADER_H
#define DATA_LOADER_H

#include <stddef.h>

typedef struct {
    char **data;
    size_t count;
} StringArray;

StringArray load_data(const char *path);
void free_data(StringArray arr);

#endif
