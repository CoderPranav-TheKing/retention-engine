//basically we need to 1. draw f(n-1) and then walk straight for n units, turn left by 90
// then draw f(n-1) and then walk straight for n, draw f(n-1), turn left, walk straight and then draw f(n-1)
#include <iostream>
using namespace std;
void printer(int n, int len){
    if (n==0){
        return;
    }
    printer(n-1,len); 
    forward(len); 
    left(90);
    printer(n-1,len);
    forward(len);
    printer(n-1,len);
    left(90);
    forward(len);
    printer(n-1,len);
}

int main(){
    turtleSim();
    int depth, int len;
    cin >> depth >> len;
    printer(depth,len);
}
