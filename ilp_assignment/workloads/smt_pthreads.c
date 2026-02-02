#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { int iters; volatile uint64_t out; } arg_t;

static inline uint64_t rotl(uint64_t x, int k){ return (x<<k) | (x>>(64-k)); }

void* worker(void* p){
    arg_t* a = (arg_t*)p;
    uint64_t x=0x9e3779b97f4a7c15ULL;
    for(int i=0;i<a->iters;i++){
        // A mix of integer ops and a branch to create bubbles.
        x ^= rotl(x, 13);
        x += 0xBF58476D1CE4E5B9ULL;
        if (x & 1) x ^= 0x94D049BB133111EBULL;
    }
    a->out = x;
    return NULL;
}

int main(int argc, char** argv){
    int iters = (argc>1)?atoi(argv[1]):3000000;
    pthread_t t0, t1;
    arg_t a0={iters,0}, a1={iters,0};

    pthread_create(&t0, NULL, worker, &a0);
    pthread_create(&t1, NULL, worker, &a1);
    pthread_join(t0, NULL);
    pthread_join(t1, NULL);

    printf("t0=%llu t1=%llu\n",(unsigned long long)a0.out,(unsigned long long)a1.out);
    return 0;
}
