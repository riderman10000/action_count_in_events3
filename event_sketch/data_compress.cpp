#include "data_compress.h"

bool is_noise(float x1, float y1, float x2, float y2, float delta = 5){
    if((abs(x1 - x2)>delta) || (abs(y1 - y2) > delta)){
        return true;
    }
    return false;
}
