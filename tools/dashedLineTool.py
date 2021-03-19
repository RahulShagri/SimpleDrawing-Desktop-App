from dearpygui.core import *
import time
import math
from db_manage import  *


def draw_dashed_line(drawing: str, p1: list[float], p2: list[float], color: list[float], thickness: int, spacing: int, tag: str):
    # Handling Horizontal lines
    if p1[1] == p2[1]:

        if p2[0] < p1[0]:
            temp = p1
            p1 = p2
            p2 = temp
            del temp

        first_point = p1[:]
        second_point = p1[:]

        temp_count = 0

        while True:
            second_point[0] += spacing

            if second_point[0] <= p2[0]:
                draw_line(drawing, first_point, second_point, color, thickness, tag=f"{tag} {temp_count}")
                temp_count+=1

            else:
                second_point[0] -= spacing
                draw_line(drawing, second_point, p2, color, thickness, tag=f"{tag} {temp_count}")
                temp_count+=1
                break

            second_point[0] += spacing

            if second_point[0] < p2[0]:
                first_point = second_point[:]
            else:
                break

    # Handling all lines except horizontal lines
    else:

        if p2[1] < p1[1]:
            temp = p1
            p1 = p2
            p2 = temp
            del temp

        length = pow((pow((p2[0] - p1[0]), 2) + pow((p2[1] - p1[1]), 2)), 0.5)

        first_point = p1

        if p2[0] >= p1[0]:
            angle = math.atan((p2[0] - p1[0]) / (p2[1] - p1[1]))

            temp_count = 0

            while True:
                x_co = first_point[0] + spacing * math.sin(angle)
                y_co = first_point[1] + spacing * math.cos(angle)

                second_point = [x_co, y_co]

                if second_point[0] <= p2[0] and second_point[1] <= p2[1]:

                    draw_line(drawing, first_point, second_point, color, thickness, tag=f"{tag} {temp_count}")
                    temp_count+=1
                    length -= spacing

                else:
                    second_point[0] -= spacing * math.sin(angle)
                    second_point[1] -= spacing * math.cos(angle)
                    draw_line(drawing, second_point, p2, color, thickness, tag=f"{tag} {temp_count}")
                    temp_count+=1
                    break

                if length >= spacing:
                    first_point = second_point
                    x_co = first_point[0] + spacing * math.sin(angle)
                    y_co = first_point[1] + spacing * math.cos(angle)
                    second_point = [x_co, y_co]
                    first_point = second_point
                    length -= spacing

                else:
                    break

        elif p2[0] < p1[0]:
            angle = math.atan((p1[0] - p2[0]) / (p2[1] - p1[1]))

            temp_count = 0

            while True:
                x_co = first_point[0] - spacing * math.sin(angle)
                y_co = first_point[1] + spacing * math.cos(angle)

                second_point = [x_co, y_co]

                if second_point[0] >= p2[0] and second_point[1] <= p2[1]:

                    draw_line(drawing, first_point, second_point, color, thickness, tag=f"{tag} {temp_count}")
                    temp_count+=1
                    length -= spacing

                else:
                    second_point[0] += spacing * math.sin(angle)
                    second_point[1] -= spacing * math.cos(angle)
                    draw_line(drawing, second_point, p2, color, thickness, tag=f"{tag} {temp_count}")
                    temp_count+=1
                    break

                if length >= spacing:
                    first_point = second_point
                    x_co = first_point[0] - spacing * math.sin(angle)
                    y_co = first_point[1] + spacing * math.cos(angle)
                    second_point = [x_co, y_co]
                    first_point = second_point
                    length -= spacing

                else:
                    break

def clear_dashed_line(drawing: str, tag: str):
    for line in range(5000):
        delete_draw_command(drawing=drawing, tag=f"{tag} {line}")

def dashedLineTool(pad_name, lineColor, lineThickness, lineSpacing):

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
                        draw_dashed_line(drawing=pad_name, p1=mouse_position, p2=[point2[0], mouse_position[1]],
                                         color=lineColor, thickness=lineThickness, spacing=lineSpacing,
                                         tag=f"dashedLine {tools.dashed_line_count}")


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

                        draw_dashed_line(drawing=pad_name, p1=mouse_position,
                                         p2=[point2[0], p2_Y],
                                         color=lineColor, thickness=lineThickness, spacing=lineSpacing,
                                         tag=f"dashedLine {tools.dashed_line_count}")

                    elif angle>60 and angle<=90:
                        draw_dashed_line(drawing=pad_name, p1=mouse_position,
                                         p2=[mouse_position[0], point2[1]],
                                         color=lineColor, thickness=lineThickness, spacing=lineSpacing,
                                         tag=f"dashedLine {tools.dashed_line_count}")
                else:
                    draw_dashed_line(drawing=pad_name, p1=mouse_position, p2=point2, color=lineColor, thickness=lineThickness, spacing=lineSpacing, tag=f"dashedLine {tools.dashed_line_count}")
                time.sleep(0.01)

                # Check if user wants to select the second point of the line
                if is_mouse_button_released(mvMouseButton_Left):
                    # If the user clicks outside the drawing pad, it is assumed that they want to terminate the tool
                    if get_active_window() != "Drawing Pad":
                        clear_dashed_line(pad_name, f"dashedLine {tools.dashed_line_count}")
                        break

                    write_db(tool="dashed line tool", point_1=str(mouse_position), point_2=str(point2), color=str(lineColor), thickness=lineThickness, spacing=lineSpacing, tag=f"dashedLine {tools.dashed_line_count}")
                    tools.dashed_line_count += 1
                    time.sleep(0.01)
                    break

                # Check if user wants to exit the line tool
                if is_mouse_button_released(mvMouseButton_Right):
                    clear_dashed_line(pad_name, f"dashedLine {tools.dashed_line_count}")
                    break

                # Check if user wants to exit the line tool
                if is_key_released(mvKey_Escape):
                    clear_dashed_line(pad_name, f"dashedLine {tools.dashed_line_count}")
                    break

                # Delete the line drawn and begin the process again till user clicks the second point or exits the tool
                clear_dashed_line(pad_name, f"dashedLine {tools.dashed_line_count}")

def get_angle(first_position, second_position):

    if second_position[0] == first_position[0]:
        return 0

    else:
        return abs(math.degrees(math.atan((second_position[1] - first_position[1]) / (second_position[0] - first_position[0]))))
