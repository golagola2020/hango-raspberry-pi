#include "Arduino.h"
#include "solded.h"


solded::solded(int distance, int line_num, int BOTH_SIDE_SPACE, int MAX_POSITION, int BUTTON_RANGE)
{
_sold_position = 0;
_distance = distance;
_line_num = line_num;
_BOTH_SIDE_SPACE = BOTH_SIDE_SPACE;
_MAX_POSITION = MAX_POSITION;
_BUTTON_RANGE = BUTTON_RANGE;
}

int solded::calculate_sold()
{
if (_BOTH_SIDE_SPACE <= _distance && _distance < (_MAX_POSITION * _BUTTON_RANGE) + _BOTH_SIDE_SPACE)
    _sold_position = ceil((_distance - _BOTH_SIDE_SPACE) / _BUTTON_RANGE + (_line_num * _MAX_POSITION)) + 1;
return _sold_position;
}
