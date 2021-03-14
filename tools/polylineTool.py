from dearpygui.core import *
import time
import math

polyLine_count = 0

def polylineTool(pad_name, lineColor, lineThickness):
    print("\nPolyline tool initiated.")

    global polyLine_count

    time.sleep(0.1)
    while True:
        if is_mouse_button_released(mvMouseButton_Left):

            # If mouse is clicked outside the Drawing Pad, exit the tool.
            if get_active_window() != "Drawing Pad":
                print("\nPolyline tool terminated.")
                return

            # Continue of clicked on the drawing pad
            first_point = get_drawing_mouse_pos()
            mouse_position = get_drawing_mouse_pos()
            time.sleep(0.01)

            while True:
                # Draw line
                point2 = get_drawing_mouse_pos()
                
                if is_key_down(mvKey_Shift):
                    angle = get_angle(mouse_position, get_drawing_mouse_pos())

                    if angle>=0 and angle<=30:
                        draw_line(pad_name, p1=mouse_position, p2=[get_drawing_mouse_pos()[0], mouse_position[1]], color=lineColor,
                                  thickness=lineThickness, tag=f"polyLine {polyLine_count}")

                        point2 = [get_drawing_mouse_pos()[0], mouse_position[1]]

                    elif angle>30 and angle<=60:

                        p2_Y = 0

                        if (get_drawing_mouse_pos()[1] - mouse_position[1]) > 0:
                            if (get_drawing_mouse_pos()[0] - mouse_position[0]) > 0:
                                p2_Y = mouse_position[1] - (mouse_position[0] - get_drawing_mouse_pos()[0])
                            else:
                                p2_Y = mouse_position[1] + (mouse_position[0] - get_drawing_mouse_pos()[0])

                        elif (get_drawing_mouse_pos()[1] - mouse_position[1]) < 0:
                            if (get_drawing_mouse_pos()[0] - mouse_position[0]) > 0:
                                p2_Y = mouse_position[1] + (mouse_position[0] - get_drawing_mouse_pos()[0])
                            else:
                                p2_Y = mouse_position[1] - (mouse_position[0] - get_drawing_mouse_pos()[0])

                        draw_line(pad_name, p1=mouse_position, p2=[get_drawing_mouse_pos()[0], p2_Y], color=lineColor,
                                  thickness=lineThickness, tag=f"polyLine {polyLine_count}")

                        point2 = [get_drawing_mouse_pos()[0], p2_Y]

                    elif angle>60 and angle<=90:
                        draw_line(pad_name, p1=mouse_position, p2=[mouse_position[0], get_drawing_mouse_pos()[1]], color=lineColor,
                                  thickness=lineThickness, tag=f"polyLine {polyLine_count}")

                        point2 = [mouse_position[0], get_drawing_mouse_pos()[1]]
                else:
                    draw_line(pad_name, p1=mouse_position, p2=point2, color=lineColor, thickness=lineThickness, tag=f"polyLine {polyLine_count}")

                time.sleep(0.01)

                # Check if user wants to select more points for the polyline
                if is_mouse_button_released(mvMouseButton_Left):
                    # If the user clicks outside the drawing pad, it is assumed that they want to terminate the tool
                    if get_active_window() != "Drawing Pad":
                        delete_draw_command(pad_name, f"polyLine {polyLine_count}")

                        if get_value("Close polyline") == True:
                            draw_line(pad_name, p1=first_point, p2=mouse_position, color=lineColor, thickness=lineThickness,
                                      tag=f"polyLine {polyLine_count}")
                            polyLine_count += 1

                        print("\nPolyline tool terminated.")
                        return

                    polyLine_count += 1
                    mouse_position = point2
                    time.sleep(0.01)

                # Check if user wants to exit the line tool
                if is_mouse_button_released(mvMouseButton_Right):
                    delete_draw_command(pad_name, f"polyLine {polyLine_count}")

                    if get_value("Close polyline") == True:
                        draw_line(pad_name, p1=first_point, p2=mouse_position, color=lineColor, thickness=lineThickness,
                                  tag=f"polyLine {polyLine_count}")
                        polyLine_count += 1

                    print("\nPolyline tool terminated.")
                    return

                # Check if user wants to exit the line tool
                if is_key_released(mvKey_Escape):
                    delete_draw_command(pad_name, f"polyLine {polyLine_count}")

                    if get_value("Close polyline") == True:
                        draw_line(pad_name, p1=first_point, p2=mouse_position, color=lineColor, thickness=lineThickness,
                                  tag=f"polyLine {polyLine_count}")
                        polyLine_count += 1

                    print("\nPolyline tool terminated.")
                    return

                # Delete the line drawn and begin the process again till user clicks the second point or exits the tool
                delete_draw_command(pad_name, f"polyLine {polyLine_count}")

def get_angle(first_position, second_position):

    if second_position[0] == first_position[0]:
        return 0

    else:
        return abs(math.degrees(math.atan((second_position[1] - first_position[1]) / (second_position[0] - first_position[0]))))
