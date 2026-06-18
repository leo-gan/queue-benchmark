#include "data_loader.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>

StringArray load_data(const char *path) {
    StringArray arr = {NULL, 0};
    DIR *d = opendir(path);
    if (d) {
        struct dirent *dir;
        size_t capacity = 10;
        arr.data = malloc(capacity * sizeof(char*));
        if (!arr.data) {
            closedir(d);
            return arr;
        }
        while ((dir = readdir(d)) != NULL) {
            if (dir->d_type == DT_REG) {
                char filepath[1024];
                snprintf(filepath, sizeof(filepath), "%s/%s", path, dir->d_name);
                FILE *f = fopen(filepath, "r");
                if (f) {
                    fseek(f, 0, SEEK_END);
                    long length = ftell(f);
                    fseek(f, 0, SEEK_SET);
                    char *buffer = malloc(length + 1);
                    if (fread(buffer, 1, length, f) != (size_t)length) {
                        free(buffer);
                        fclose(f);
                        continue;
                    }
                    buffer[length] = '\0';
                    fclose(f);

                    if (arr.count >= capacity) {
                        capacity *= 2;
                        char **new_data = realloc(arr.data, capacity * sizeof(char*));
                        if (!new_data) {
                            free_data(arr);
                            closedir(d);
                            return (StringArray){NULL, 0};
                        }
                        arr.data = new_data;
                    }
                    arr.data[arr.count++] = buffer;
                }
            }
        }
        closedir(d);
    }
    return arr;
}

void free_data(StringArray arr) {
    for (size_t i = 0; i < arr.count; i++) {
        free(arr.data[i]);
    }
    free(arr.data);
}
