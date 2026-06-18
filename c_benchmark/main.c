#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <pthread.h>
#include <zmq.h>
#include "../common/data_loader.h"
#include "../common/stats.h"

unsigned long long get_time_ns() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (unsigned long long)ts.tv_sec * 1000000000ULL + ts.tv_nsec;
}

typedef struct {
    StringArray data;
    void *ctx;
} ZmqArgs;

void *zmq_producer(void *arg) {
    ZmqArgs *args = (ZmqArgs *)arg;
    void *socket = zmq_socket(args->ctx, ZMQ_PUSH);
    zmq_connect(socket, "inproc://test");

    for (size_t i = 0; i < args->data.count; i++) {
        zmq_send(socket, args->data.data[i], strlen(args->data.data[i]), 0);
    }
    zmq_close(socket);
    return NULL;
}

void benchmark_zmq(StringArray data, size_t total_bytes) {
    void *ctx = zmq_ctx_new();
    void *socket = zmq_socket(ctx, ZMQ_PULL);
    zmq_bind(socket, "inproc://test");

    ZmqArgs args = {data, ctx};
    pthread_t producer_thread;
    pthread_create(&producer_thread, NULL, zmq_producer, &args);

    unsigned long long *times_ns = malloc(data.count * sizeof(unsigned long long));
    if (!times_ns) {
        perror("Failed to allocate memory for times_ns");
        return;
    }
    char buffer[65536]; // 64KB buffer is safe for stack and sufficient for benchmark payloads

    for (size_t i = 0; i < data.count; i++) {
        unsigned long long start = get_time_ns();
        zmq_recv(socket, buffer, sizeof(buffer), 0);
        unsigned long long end = get_time_ns();
        times_ns[i] = end - start;
    }

    pthread_join(producer_thread, NULL);
    zmq_close(socket);
    zmq_ctx_destroy(ctx);

    StatsData stats = calculate_stats(times_ns, data.count, total_bytes);
    print_stats("ZeroMQ inproc", stats);

    free(times_ns);
}

int main(int argc, char **argv) {
    const char *data_path = argc > 1 ? argv[1] : "../datasets/test_folder";
    printf("Loading data from: %s\n", data_path);

    StringArray data = load_data(data_path);
    size_t total_bytes = 0;
    for (size_t i = 0; i < data.count; i++) {
        total_bytes += strlen(data.data[i]);
    }
    printf("Loaded %zu records, total size: %zu bytes\n", data.count, total_bytes);

    if (data.count > 0) {
        benchmark_zmq(data, total_bytes);
    } else {
        printf("Warning: No data loaded. Cannot run benchmarks.\n");
    }

    free_data(data);
    printf("C benchmarks completed.\n");
    return 0;
}
