#ifndef _DATA_COMPRESS_H
#define _DATA_COMPRESS_H

#include <math.h>

bool is_noise(float x1, float y1, float x2, float y2, float delta = 5);

/* 
    current plan accept the array of the x and y along with a value that is suppose to 
    limit the number of iteration to follow like a window size.
    because importing all the values doesnot make any sense right 
    and further more memory and resources...
*/
void compress_by_manhattan(float &x, float &y);


#endif 