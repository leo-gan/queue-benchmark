CC = gcc
CFLAGS = -Wall -Wextra -O3 -I../common
LDFLAGS = -lzmq -lpthread -lm

SRCS = main.c ../common/data_loader.c ../common/stats.c
OBJS = $(SRCS:.c=.o)

benchmark: $(OBJS)
	$(CC) $(OBJS) -o benchmark $(LDFLAGS)

clean:
	rm -f $(OBJS) benchmark
