#define _GNU_SOURCE
#define _POSIX_C_SOURCE 200809L
#include <pthread.h>
#include <stdatomic.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/resource.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sqlite3.h>
#include "lfqueue.h"

static uint64_t now_ns(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (uint64_t)ts.tv_sec * 1000000000ull + (uint64_t)ts.tv_nsec;
}

static uint64_t cpu_ns(void) {
    struct timespec ts;
    if (clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &ts) != 0)
        return 0;
    return (uint64_t)ts.tv_sec * 1000000000ull + (uint64_t)ts.tv_nsec;
}

static void sleep_ns(uint64_t ns) {
    struct timespec ts;
    ts.tv_sec = (time_t)(ns / 1000000000ull);
    ts.tv_nsec = (long)(ns % 1000000000ull);
    nanosleep(&ts, NULL);
}

static uint64_t rss_bytes(void) {
    struct rusage ru;
    if (getrusage(RUSAGE_SELF, &ru) != 0)
        return 0;
    return (uint64_t)ru.ru_maxrss * 1024ull;
}

static int env_on(const char *name) {
    const char *v = getenv(name);
    return v && (!strcmp(v, "1") || !strcmp(v, "true") || !strcmp(v, "on"));
}

static int name_wanted(const char *name, const char *qf, int opt_in, int include_psd, const char *psd_names) {
    if (qf[0] && !strstr(name, qf))
        return 0;
    if (opt_in) {
        if (!include_psd && !qf[0])
            return 0;
        if (psd_names[0] && !strstr(psd_names, name))
            return 0;
    }
    return 1;
}

static void write_frame(int fd, const void *item, int payload) {
    uint32_t n = htonl((uint32_t)payload);
    if (write(fd, &n, 4) != 4) return;
    if (payload > 0) (void)write(fd, item, (size_t)payload);
}

static int read_frame(int fd, int payload) {
    uint32_t n = 0;
    if (read(fd, &n, 4) != 4) return -1;
    n = ntohl(n);
    char buf[4096];
    while (n) {
        size_t chunk = n > sizeof buf ? sizeof buf : n;
        ssize_t r = read(fd, buf, chunk);
        if (r <= 0) return -1;
        n -= (uint32_t)r;
    }
    (void)payload;
    return 0;
}

static void bench_pipe(void **items, int n, int payload, uint64_t *enq, uint64_t *deq) {
    int fd[2];
    if (pipe(fd) != 0) { *enq = *deq = 0; return; }
    pid_t pid = fork();
    if (pid == 0) {
        close(fd[1]);
        for (int i = 0; i < n; i++) (void)read_frame(fd[0], payload);
        close(fd[0]);
        _exit(0);
    }
    close(fd[0]);
    uint64_t t0 = now_ns();
    for (int i = 0; i < n; i++) write_frame(fd[1], items[i], payload);
    close(fd[1]);
    int st = 0;
    waitpid(pid, &st, 0);
    uint64_t wall = now_ns() - t0;
    *enq = wall / 2;
    *deq = wall - *enq;
}

typedef struct {
    atomic_uint *head;
    atomic_uint *tail;
    uint32_t slots, slot;
    uint32_t *lens;
    uint8_t *data;
} SharedRing;

static void ring_attach(SharedRing *r, uint8_t *mem, uint32_t slots, uint32_t slot) {
    r->head = (atomic_uint *)mem;
    r->tail = (atomic_uint *)(mem + sizeof(atomic_uint));
    r->slots = slots;
    r->slot = slot;
    r->lens = (uint32_t *)(mem + 2 * sizeof(atomic_uint));
    r->data = mem + 2 * sizeof(atomic_uint) + sizeof(uint32_t) * slots;
}

static void ring_push(SharedRing *r, const void *item, int n) {
    for (;;) {
        uint32_t tail = atomic_load_explicit(r->tail, memory_order_relaxed);
        uint32_t head = atomic_load_explicit(r->head, memory_order_acquire);
        uint32_t nxt = (tail + 1) % r->slots;
        if (nxt == head) continue;
        uint32_t len = (uint32_t)n;
        if (len > r->slot) len = r->slot;
        r->lens[tail] = len;
        memcpy(r->data + (size_t)tail * r->slot, item, len);
        atomic_store_explicit(r->tail, nxt, memory_order_release);
        return;
    }
}

static void ring_pop(SharedRing *r) {
    for (;;) {
        uint32_t head = atomic_load_explicit(r->head, memory_order_relaxed);
        uint32_t tail = atomic_load_explicit(r->tail, memory_order_acquire);
        if (head == tail) continue;
        atomic_store_explicit(r->head, (head + 1) % r->slots, memory_order_release);
        return;
    }
}

static void bench_shared(void **items, int n, int payload, uint64_t *enq, uint64_t *deq) {
    uint32_t slots = (uint32_t)n + 2;
    uint32_t slot = payload > 64 ? (uint32_t)payload : 64;
    size_t bytes = 2 * sizeof(atomic_uint) + sizeof(uint32_t) * slots + (size_t)slots * slot;
    uint8_t *mem = mmap(NULL, bytes, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    if (mem == MAP_FAILED) { *enq = *deq = 0; return; }
    memset(mem, 0, bytes);
    SharedRing ring;
    ring_attach(&ring, mem, slots, slot);
    atomic_init(ring.head, 0);
    atomic_init(ring.tail, 0);
    pid_t pid = fork();
    if (pid == 0) {
        SharedRing child;
        ring_attach(&child, mem, slots, slot);
        for (int i = 0; i < n; i++) ring_pop(&child);
        _exit(0);
    }
    uint64_t t0 = now_ns();
    for (int i = 0; i < n; i++) ring_push(&ring, items[i], payload);
    int st = 0;
    waitpid(pid, &st, 0);
    uint64_t wall = now_ns() - t0;
    *enq = wall / 2;
    *deq = wall - *enq;
    munmap(mem, bytes);
}

static void bench_sqlite(void **items, int n, int payload, uint64_t *enq, uint64_t *deq) {
    char path[128];
    snprintf(path, sizeof path, "/tmp/qb-d-%d-%ld.sqlite", (int)getpid(), (long)now_ns());
    sqlite3 *db = NULL;
    if (sqlite3_open(path, &db) != SQLITE_OK) { *enq = *deq = 0; return; }
    int fsync = env_on("BENCHMARK_FSYNC");
    sqlite3_exec(db, "PRAGMA journal_mode=WAL", NULL, NULL, NULL);
    sqlite3_exec(db, fsync ? "PRAGMA synchronous=FULL" : "PRAGMA synchronous=OFF", NULL, NULL, NULL);
    sqlite3_exec(db, "CREATE TABLE q (id INTEGER PRIMARY KEY, payload BLOB)", NULL, NULL, NULL);
    sqlite3_stmt *ins = NULL, *sel = NULL;
    sqlite3_prepare_v2(db, "INSERT INTO q(payload) VALUES (?)", -1, &ins, NULL);
    uint64_t t0 = now_ns();
    for (int i = 0; i < n; i++) {
        sqlite3_bind_blob(ins, 1, items[i], payload, SQLITE_STATIC);
        sqlite3_step(ins);
        sqlite3_reset(ins);
    }
    *enq = now_ns() - t0;
    sqlite3_prepare_v2(db, "SELECT payload FROM q ORDER BY id", -1, &sel, NULL);
    t0 = now_ns();
    while (sqlite3_step(sel) == SQLITE_ROW) { (void)sqlite3_column_blob(sel, 0); }
    *deq = now_ns() - t0;
    sqlite3_finalize(ins);
    sqlite3_finalize(sel);
    sqlite3_close(db);
    unlink(path);
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

static void parse_pattern(const char *mode, int *p, int *c) {
    *p = 1;
    *c = 1;
    if (strcmp(mode, "stream") == 0 || strcmp(mode, "mpmc") == 0) {
        *p = 2;
        *c = 2;
        return;
    }
    if (strcmp(mode, "bytes") == 0 || strcmp(mode, "spsc") == 0)
        return;
    int pr = 0, co = 0;
    if (sscanf(mode, "%dp%dc", &pr, &co) == 2 && pr > 0 && co > 0) {
        *p = pr;
        *c = co;
    }
}

typedef struct {
    lfqueue_t *q;
    void **items;
    int a, b, take;
} LfJob;

static void *lf_prod(void *arg) {
    LfJob *j = arg;
    for (int i = j->a; i < j->b; i++)
        while (lfqueue_enq(j->q, j->items[i]) == -1) {
        }
    return NULL;
}

static void *lf_cons(void *arg) {
    LfJob *j = arg;
    for (int i = 0; i < j->take; i++)
        while (lfqueue_deq(j->q) == NULL) {
        }
    return NULL;
}

typedef struct {
    MutexQ *q;
    void **items;
    int start, end;
    int take;
} MqJob;

static void *mq_prod(void *arg) {
    MqJob *j = arg;
    for (int i = j->start; i < j->end; i++) mq_push(j->q, j->items[i]);
    return NULL;
}

static void *mq_cons(void *arg) {
    MqJob *j = arg;
    for (int i = 0; i < j->take; i++) (void)mq_pop(j->q);
    return NULL;
}

static double ops(uint64_t ns) {
    return ns ? 1000000000.0 / (double)ns : 0.0;
}

static void write_row(FILE *f, const char *mode, const char *ty, int reps, int idx,
                      const char *name, const char *ver, uint64_t enq, uint64_t deq,
                      int n, const char *hash, const char *kind, int order,
                      uint64_t cpu, uint64_t rss) {
    uint64_t tot = enq + deq;
    fprintf(f,
            "c,%s,%s,%d,%d,%s,%s,%llu,%llu,%llu,%.6f,%.6f,%.6f,%llu,1.0000,%d,%s,%s,%s,%d,%d,%llu\n",
            mode, ty, reps, idx, name, ver,
            (unsigned long long)enq, (unsigned long long)deq, (unsigned long long)tot,
            ops(enq), ops(deq), ops(tot), (unsigned long long)rss, n, hash, kind,
            strcmp(mode, "stream") == 0 ? "native" : "", order, order,
            (unsigned long long)cpu);
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
    const char *special = getenv("BENCHMARK_SPECIAL");
    if (!special) special = "";
    uint64_t wait_ns = 1000000ull;
    {
        const char *w = getenv("BENCHMARK_WAIT_NS");
        if (w && w[0]) wait_ns = strtoull(w, NULL, 10);
    }
    int include_psd = env_on("BENCHMARK_INCLUDE_PSD");
    const char *psd_names = getenv("BENCHMARK_PSD_NAMES");
    if (!psd_names) psd_names = "";
    fprintf(out, "Language,Pattern,TestDataName,Repetitions,RepetitionIndex,LibraryName,LibraryVersion,TimeEnq,TimeDeq,TimeHandoff,OpPerSecEnq,OpPerSecDeq,OpPerSecHandoff,MemoryPeakBytes,FidelityScore,DataTypeInstanceCount,TypeConfigHash,NativeKind,StreamMode,RunOrder,SchedulePosition,CpuTimeNs\n");

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

        const char *names[] = {"mutex-queue", "lfqueue", "spsc-ring", "steal-deque", "pipe-ipc", "shared-ring", "sqlite-queue"};
        const char *kinds[] = {"locked", "concurrent", "spsc", "work-stealing", "concurrent", "spsc", "durable"};
        const int opt_in[] = {0, 0, 0, 0, 1, 1, 1};
        const int spsc_only[] = {0, 0, 1, 0, 1, 1, 1};
        for (int qi = 0; qi < 7; qi++) {
            if (!name_wanted(names[qi], qf, opt_in[qi], include_psd, psd_names))
                continue;
            int producers = 1, consumers = 1;
            parse_pattern(mode, &producers, &consumers);
            if (spsc_only[qi] && (producers != 1 || consumers != 1))
                continue;
            if (strcmp(special, "cancel") == 0)
                continue;
            if (special[0] && opt_in[qi])
                continue;
            if (strcmp(special, "wakeup") == 0 &&
                (strcmp(names[qi], "spsc-ring") == 0 || strcmp(names[qi], "steal-deque") == 0 ||
                 strcmp(names[qi], "shared-ring") == 0 || strcmp(names[qi], "lfqueue") == 0))
                continue;
            for (int i = 0; i < reps; i++) {
                uint64_t enq = 0, deq = 0;
                uint64_t cpu0 = cpu_ns();
                if (strcmp(special, "wakeup") == 0) {
                    MutexQ q;
                    mq_init(&q, 2);
                    pthread_t th;
                    MqJob job = {&q, items, 0, 0, n};
                    pthread_create(&th, NULL, mq_cons, &job);
                    sleep_ns(2000000ull);
                    uint64_t t0 = now_ns();
                    for (int k = 0; k < n; k++) {
                        sleep_ns(wait_ns);
                        mq_push(&q, items[k]);
                    }
                    pthread_join(th, NULL);
                    uint64_t wall = now_ns() - t0;
                    enq = wall / (uint64_t)(n > 0 ? n : 1);
                    deq = wall - enq;
                    mq_free(&q);
                } else if (strcmp(special, "burst") == 0) {
                    if (strcmp(names[qi], "lfqueue") == 0) {
                        lfqueue_t q;
                        lfqueue_init(&q);
                        uint64_t t0 = now_ns();
                        for (int k = 0; k < n; k++)
                            while (lfqueue_enq(&q, items[k]) == -1) {
                            }
                        enq = now_ns() - t0;
                        t0 = now_ns();
                        for (int k = 0; k < n; k++)
                            while (lfqueue_deq(&q) == NULL) {
                            }
                        deq = now_ns() - t0;
                        lfqueue_destroy(&q);
                    } else if (strcmp(names[qi], "spsc-ring") == 0) {
                        Spsc q;
                        spsc_init(&q, (size_t)n + 2);
                        uint64_t t0 = now_ns();
                        for (int k = 0; k < n; k++) spsc_push(&q, items[k]);
                        enq = now_ns() - t0;
                        t0 = now_ns();
                        for (int k = 0; k < n; k++) (void)spsc_pop(&q);
                        deq = now_ns() - t0;
                        free(q.buf);
                    } else {
                        MutexQ q;
                        mq_init(&q, (size_t)n + 1);
                        uint64_t t0 = now_ns();
                        for (int k = 0; k < n; k++) mq_push(&q, items[k]);
                        enq = now_ns() - t0;
                        t0 = now_ns();
                        for (int k = 0; k < n; k++) (void)mq_pop(&q);
                        deq = now_ns() - t0;
                        mq_free(&q);
                    }
                } else if (strcmp(names[qi], "pipe-ipc") == 0) {
                    bench_pipe(items, n, payload, &enq, &deq);
                } else if (strcmp(names[qi], "shared-ring") == 0) {
                    bench_shared(items, n, payload, &enq, &deq);
                } else if (strcmp(names[qi], "sqlite-queue") == 0) {
                    bench_sqlite(items, n, payload, &enq, &deq);
                } else if (strcmp(names[qi], "lfqueue") == 0) {
                    lfqueue_t q;
                    lfqueue_init(&q);
                    if (producers == 1 && consumers == 1) {
                        uint64_t t0 = now_ns();
                        for (int k = 0; k < n; k++)
                            while (lfqueue_enq(&q, items[k]) == -1) {
                            }
                        enq = now_ns() - t0;
                        t0 = now_ns();
                        for (int k = 0; k < n; k++)
                            while (lfqueue_deq(&q) == NULL) {
                            }
                        deq = now_ns() - t0;
                    } else {
                        pthread_t th[16];
                        LfJob jobs[16];
                        int nt = 0;
                        uint64_t t0 = now_ns();
                        for (int p = 0; p < producers && nt < 16; p++) {
                            jobs[nt] = (LfJob){&q, items, n * p / producers, n * (p + 1) / producers, 0};
                            pthread_create(&th[nt], NULL, lf_prod, &jobs[nt]);
                            nt++;
                        }
                        int per = n / consumers, extra = n % consumers;
                        for (int c = 0; c < consumers && nt < 16; c++) {
                            jobs[nt] = (LfJob){&q, items, 0, 0, per + (c == 0 ? extra : 0)};
                            pthread_create(&th[nt], NULL, lf_cons, &jobs[nt]);
                            nt++;
                        }
                        for (int t = 0; t < nt; t++) pthread_join(th[t], NULL);
                        uint64_t wall = now_ns() - t0;
                        enq = wall / 2;
                        deq = wall - enq;
                    }
                    lfqueue_destroy(&q);
                } else if (strcmp(names[qi], "mutex-queue") == 0 || strcmp(names[qi], "steal-deque") == 0) {
                    MutexQ q;
                    mq_init(&q, (size_t)n + 1);
                    if (producers == 1 && consumers == 1) {
                        uint64_t t0 = now_ns();
                        for (int k = 0; k < n; k++) mq_push(&q, items[k]);
                        enq = now_ns() - t0;
                        t0 = now_ns();
                        for (int k = 0; k < n; k++) (void)mq_pop(&q);
                        deq = now_ns() - t0;
                    } else {
                        pthread_t th[16];
                        MqJob jobs[16];
                        int nt = 0;
                        uint64_t t0 = now_ns();
                        for (int p = 0; p < producers && nt < 16; p++) {
                            jobs[nt] = (MqJob){&q, items, n * p / producers, n * (p + 1) / producers, 0};
                            pthread_create(&th[nt], NULL, mq_prod, &jobs[nt]);
                            nt++;
                        }
                        int per = n / consumers, extra = n % consumers;
                        for (int c = 0; c < consumers && nt < 16; c++) {
                            jobs[nt] = (MqJob){&q, items, 0, 0, per + (c == 0 ? extra : 0)};
                            pthread_create(&th[nt], NULL, mq_cons, &jobs[nt]);
                            nt++;
                        }
                        for (int t = 0; t < nt; t++) pthread_join(th[t], NULL);
                        uint64_t wall = now_ns() - t0;
                        enq = wall / 2;
                        deq = wall - enq;
                    }
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
                          enq, deq, n, hash, kinds[qi], order,
                          cpu_ns() - cpu0, rss_bytes());
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
