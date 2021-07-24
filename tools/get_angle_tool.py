import math


def get_angle(first_position, second_position):
    # Returns the angle between two lines
    if second_position[0] == first_position[0]:
        return 0

    else:
        return abs(math.degrees(math.atan((second_position[1] - first_position[1]) / (second_position[0] - first_position[0]))))
