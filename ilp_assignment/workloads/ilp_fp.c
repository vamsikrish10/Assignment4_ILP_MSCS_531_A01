#include <stdio.h>
#include <stdlib.h>

int main(int argc, char** argv){
    const int N = (argc > 1) ? atoi(argv[1]) : 2000000;
    volatile double a=1.1,b=2.2,c=3.3,d=4.4;
    for(int i=0;i<N;i++){
        // Mix independent FP ops with some dependence.
        a = a * 1.0000001 + 0.0000003;
        b = b + 0.0000007 * a;
        c = c * 0.9999999 + b;
        d = d + a * b - c;
    }
    printf("fp: %.6f\n", (double)(a+b+c+d));
    return 0;
}
