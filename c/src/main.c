#define _POSIX_C_SOURCE 199309L
#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static uint64_t now_ns(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (uint64_t)ts.tv_sec * 1000000000ull + (uint64_t)ts.tv_nsec;
}

typedef struct {
    void **buf;
    size_t cap, head, tail, count;
    pthread_mutex_t mu;
    pthread_cond_t not_empty;
    pthread_cond_t not_full;
} MutexQ;

static void mq_init(MutexQ *q, size_t cap) {
    q->buf = calloc(cap, sizeof(void *));
    q->cap = cap;
    q->head = q->tail = q->count = 0;
    pthread_mutex_init(&q->mu, NULL);
    pthread_cond_init(&q->not_empty, NULL);
    pthread_cond_init(&q->not_full, NULL);
}

static void mq_push(MutexQ *q, void *item) {
    pthread_mutex_lock(&q->mu);
    while (q->count == q->cap) pthread_cond_wait(&q->not_full, &q->mu);
    q->buf[q->tail] = item;
    q->tail = (q->tail + 1) % q->cap;
    q->count++;
    pthread_cond_signal(&q->not_empty);
    pthread_mutex_unlock(&q->mu);
}

static void *mq_pop(MutexQ *q) {
    pthread_mutex_lock(&q->mu);
    while (q->count == 0) pthread_cond_wait(&q->not_empty, &q->mu);
    void *item = q->buf[q->head];
    q->head = (q->head + 1) % q->cap;
    q->count--;
    pthread_cond_signal(&q->not_full);
    pthread_mutex_unlock(&q->mu);
    return item;
}

static void mq_free(MutexQ *q) {
    pthread_mutex_destroy(&q->mu);
    pthread_cond_destroy(&q->not_empty);
    pthread_cond_destroy(&q->not_full);
    free(q->buf);
}

typedef struct {
    void **buf;
    size_t cap, head, tail;
} Spsc;

static void spsc_init(Spsc *q, size_t cap) {
    q->buf = calloc(cap, sizeof(void *));
    q->cap = cap;
    q->head = q->tail = 0;
}

static void spsc_push(Spsc *q, void *item) {
    size_t next = (q->tail + 1) % q->cap;
    while (next == q->head) { /* spin if full — size is n+1 so should not */ }
    q->buf[q->tail] = item;
    q->tail = next;
}

static void *spsc_pop(Spsc *q) {
    while (q->head == q->tail) { }
    void *item = q->buf[q->head];
    q->head = (q->head + 1) % q->cap;
    return item;
}

static double ops(uint64_t ns) {
    return ns ? 1000000000.0 / (double)ns : 0.0;
}

static void write_row(FILE *f, const char *mode, const char *ty, int reps, int idx,
                      const char *name, const char *ver, uint64_t enq, uint64_t deq,
                      size_t size, int n, const char *hash, const char *kind, int order) {
    uint64_t tot = enq + deq;
    fprintf(f,
            "c,%s,%s,%d,%d,%s,%s,%llu,%llu,%zu,%llu,%.6f,%.6f,%.6f,0,1.0000,%d,%s,0,0,%s,%s,%d,%d\n",
            mode, ty, reps, idx, name, ver,
            (unsigned long long)enq, (unsigned long long)deq, size, (unsigned long long)tot,
            ops(enq), ops(deq), ops(tot), n, hash, kind,
            strcmp(mode, "stream") == 0 ? "native" : "", order, order);
}

int main(int argc, char **argv) {
    int reps = argc > 1 ? atoi(argv[1]) : 10;
    const char *qf = argc > 2 ? argv[2] : "";
    const char *df = argc > 3 ? argv[3] : "";
    const char *cells = getenv("BENCHMARK_CELLS_TSV");
    if (!cells) {
        fprintf(stderr, "BENCHMARK_CELLS_TSV not set\n");
        return 1;
    }
    const char *logdir = getenv("LOG_DIR");
    if (!logdir) logdir = "../logs/c";
    char outdir[1024];
    snprintf(outdir, sizeof outdir, "%s", logdir);
    char cmd[1200];
    snprintf(cmd, sizeof cmd, "mkdir -p '%s'", outdir);
    system(cmd);
    const char *ts = getenv("BENCHMARK_TS");
    if (!ts) ts = "run";
    char outpath[1200];
    snprintf(outpath, sizeof outpath, "%s/%s.csv", outdir, ts);
    FILE *out = fopen(outpath, "w");
    if (!out) {
        perror(outpath);
        return 1;
    }
    fprintf(out, "Language,StringOrStream,TestDataName,Repetitions,RepetitionIndex,SerializerName,SerializerVersion,TimeSer,TimeDeser,Size,TimeSerAndDeser,OpPerSecSer,OpPerSecDeser,OpPerSecSerAndDeser,MemoryPeakBytes,FidelityScore,DataTypeInstanceCount,TypeConfigHash,SizeGzip,SizeZstd,NativeKind,StreamMode,RunOrder,SchedulePosition\n");

    FILE *cf = fopen(cells, "r");
    if (!cf) {
        perror(cells);
        return 1;
    }
    char line[1024];
    fgets(line, sizeof line, cf); /* header */
    int order = 0;
    while (fgets(line, sizeof line, cf)) {
        char type_id[64], mode[32], hash[64];
        int payload = 0, n = 0;
        if (sscanf(line, "%63s %d %d %31s %63s", type_id, &payload, &n, mode, hash) != 5)
            continue;
        if (df[0] && !strstr(type_id, df))
            continue;
        char *item = malloc((size_t)payload);
        memset(item, 'a', (size_t)payload);
        void **items = calloc((size_t)n, sizeof(void *));
        for (int i = 0; i < n; i++) items[i] = item;
        size_t size = (size_t)payload * (size_t)n;
        const char *names[] = {"mutex-queue", "spsc-ring"};
        for (int qi = 0; qi < 2; qi++) {
            if (qf[0] && !strstr(names[qi], qf))
                continue;
            if (strcmp(mode, "stream") == 0 && strcmp(names[qi], "spsc-ring") == 0)
                continue;
            for (int i = 0; i < reps; i++) {
                uint64_t enq = 0, deq = 0;
                if (strcmp(names[qi], "mutex-queue") == 0) {
                    MutexQ q;
                    mq_init(&q, (size_t)n + 1);
                    uint64_t t0 = now_ns();
                    for (int k = 0; k < n; k++) mq_push(&q, items[k]);
                    enq = now_ns() - t0;
                    t0 = now_ns();
                    for (int k = 0; k < n; k++) (void)mq_pop(&q);
                    deq = now_ns() - t0;
                    mq_free(&q);
                } else {
                    Spsc q;
                    spsc_init(&q, (size_t)n + 2);
                    uint64_t t0 = now_ns();
                    for (int k = 0; k < n; k++) spsc_push(&q, items[k]);
                    enq = now_ns() - t0;
                    t0 = now_ns();
                    for (int k = 0; k < n; k++) (void)spsc_pop(&q);
                    deq = now_ns() - t0;
                    free(q.buf);
                }
                write_row(out, mode, type_id, reps, i, names[qi], "0.1.0",
                          enq, deq, size, n, hash,
                          strcmp(names[qi], "spsc-ring") == 0 ? "spsc" : "locked", order);
                order++;
            }
        }
        free(items);
        free(item);
    }
    fclose(cf);
    fclose(out);
    printf("Wrote %s\n", outpath);
    return 0;
}
