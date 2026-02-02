#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static inline uint64_t xorshift64(uint64_t *s){
    uint64_t x = *s;
    x ^= x << 13; x ^= x >> 7; x ^= x << 17;
    *s = x;
    return x;
}

int main(int argc, char** argv){
    const int N = (argc > 1) ? atoi(argv[1]) : 2000000;
    uint64_t s = 0x123456789abcdefULL;
    volatile uint64_t a=1,b=2,c=3,d=4;
    // Mix: dependent chain + independent ops to expose ILP and its limits.
    for(int i=0;i<N;i++){
        uint64_t r1 = xorshift64(&s);
        uint64_t r2 = xorshift64(&s);
        uint64_t r3 = xorshift64(&s);

        // Dependent chain (latency-bound)
        a = (a * 1664525ULL + 1013904223ULL) ^ (r1 & 0xffff);

        // Mostly independent (throughput-bound)
        b = b + (r2 & 0xff);
        c = c ^ (r3 << (r2 & 7));
        d = d + b + c;

        // Control dependency: unpredictable-ish branch
        if ((r1 ^ r2) & 1) { a += d; } else { a ^= d; }
    }
    printf("done: %llu\n",(unsigned long long)(a+b+c+d));
    return 0;
}
