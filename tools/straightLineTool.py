from dearpygui.core import *
import time
import math
from db_manage import *

def straightLineTool(pad_name, lineColor, lineThickness):

    time.sleep(0.1)

    while True:
        # Begin drawing when left mouse button is released
        if is_mouse_button_released(mvMouseButton_Left):

            # If mouse is clicked outside the Drawing Pad, exit the tool.
            if get_active_window() != "Drawing Pad":
                break

            # Continue of clicked on the drawing pad
            mouse_position = get_drawing_mouse_pos()
            time.sleep(0.01)

            while True:
                # Draw line
                point2 = get_drawing_mouse_pos()
                if is_key_down(mvKey_Shift):
                    angle = get_angle(mouse_position, point2)

                    if angle>=0 and angle<=30:
                        point2 = [point2[0], mouse_position[1]]
                        draw_line(pad_name, p1=mouse_position, p2=point2, color=lineColor,
                                  thickness=lineThickness, tag=f"straightLine {tools.straight_line_count}")

                    elif angle>30 and angle<=60:

                        p2_Y = 0

                        if (point2[1] - mouse_position[1]) > 0:
                            if (point2[0] - mouse_position[0]) > 0:
                                p2_Y = mouse_position[1] - (mouse_position[0] - point2[0])
                            else:
                                p2_Y = mouse_position[1] + (mouse_position[0] - point2[0])

                        elif (point2[1] - mouse_position[1]) < 0:
                            if (point2[0] - mouse_position[0]) > 0:
                                p2_Y = mouse_position[1] + (mouse_position[0] - point2[0])
                            else:
                                p2_Y = mouse_position[1] - (mouse_position[0] - point2[0])

                        point2 = [point2[0], p2_Y]
                        draw_line(pad_name, p1=mouse_position, p2=point2, color=lineColor,
                                  thickness=lineThickness, tag=f"straightLine {tools.straight_line_count}")

                    elif angle>60 and angle<=90:
                        point2 = [mouse_position[0], point2[1]]
                        draw_line(pad_name, p1=mouse_position, p2=point2, color=lineColor,
                                  thickness=lineThickness, tag=f"straightLine {tools.straight_line_count}")

                else:
                    draw_line(pad_name, p1=mouse_position, p2=point2, color=lineColor,
                              thickness=lineThickness, tag=f"straightLine {tools.straight_line_count}")

                time.sleep(0.01)

                # Check if user wants to select the second point of the line
                if is_mouse_button_released(mvMouseButton_Left):
                    # If the user clicks outside the drawing pad, it is assumed that they want to terminate the tool
                    if get_active_window() != "Drawing Pad":
                        delete_draw_command(pad_name, f"straightLine {tools.straight_line_count}")
                        break

                    write_db(tool="straight line tool", point_1=str(mouse_position), point_2=str(point2), color=str(lineColor), thickness=lineThickness, tag=f"straightLine {tools.straight_line_count}")
                    tools.straight_line_count += 1
                    time.sleep(0.01)
                    break

                # Check if user wants to exit the line tool
                if is_mouse_button_released(mvMouseButton_Right):
                    delete_draw_command(pad_name, f"straightLine {tools.straight_line_count}")
                    break

                # Check if user wants to exit the line tool
                if is_key_released(mvKey_Escape):
                    delete_draw_command(pad_name, f"straightLine {tools.straight_line_count}")
                    break

                # Delete the line drawn and begin the process again till user clicks the second point or exits the tool
                delete_draw_command(pad_name, f"straightLine {tools.straight_line_count}")

def get_angle(first_position, second_position):

    if second_position[0] == first_position[0]:
        return 0

    else:
        return abs(math.degrees(math.atan((second_position[1] - first_position[1]) / (second_position[0] - first_position[0]))))
