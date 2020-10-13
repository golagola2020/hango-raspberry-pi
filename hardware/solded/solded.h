#ifndef solded_h
#define solded_h

#include "Arduino.h"

class solded
{
public:
solded(int distance, int line_num, int BOTH_SIDE_SPACE, int MAX_POSITION, int BUTTON_RANGE);
int calculate_sold();
private:
int _sold_position;
int _distance;
int _line_num;
int _BOTH_SIDE_SPACE;
int _MAX_POSITION;
int _BUTTON_RANGE;
};

#endif
