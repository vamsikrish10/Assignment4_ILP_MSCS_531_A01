#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char** argv){
    const size_t N = (argc > 1) ? (size_t)atoll(argv[1]) : (1<<20);
    const size_t stride = (argc > 2) ? (size_t)atoll(argv[2]) : 64/sizeof(uint64_t);

    uint64_t *arr = (uint64_t*)malloc(N * sizeof(uint64_t));
    if(!arr){ perror("malloc"); return 1; }
    for(size_t i=0;i<N;i++) arr[i]=i*1315423911u;

    volatile uint64_t sum = 0;
    // Memory-level behavior + some ILP via unrolling.
    for(size_t i=0;i+4*stride < N; i += 4*stride){
        sum += arr[i];
        sum += arr[i+stride];
        sum += arr[i+2*stride];
        sum += arr[i+3*stride];
    }
    printf("sum: %llu\n",(unsigned long long)sum);
    free(arr);
    return 0;
}
