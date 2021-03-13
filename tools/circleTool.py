from dearpygui.core import *
from dearpygui.simple import *
import math
import time

circleCount = 0

def circleTool(pad_name, lineColor, lineThickness, fillCircle):
    print("\nCircle tool initiated.")

    global circleCount    #Keeping a track of the number of circles

    time.sleep(0.1)

    while True:
        # Begin drawing when left mouse button is released
        if is_mouse_button_released(mvMouseButton_Left):

            # If mouse is clicked outside the Drawing Pad, exit the tool.
            if get_active_window() != "Drawing Pad":
                print("\nCircle tool terminated.")
                return

            # Continue of clicked on the drawing pad
            mouse_position = get_drawing_mouse_pos()
            time.sleep(0.01)

            while True:
                # Draw line
                radius = math.sqrt(math.pow(mouse_position[0] - get_drawing_mouse_pos()[0], 2) + math.pow(mouse_position[1] - get_drawing_mouse_pos()[1], 2))
                draw_circle(pad_name, center=mouse_position, radius=radius, color=lineColor, thickness=lineThickness, fill=fillCircle, tag=f"circle {circleCount}")
                time.sleep(0.01)
                line_flag = 1

                # Check if user wants to select the second point
                if is_mouse_button_released(mvMouseButton_Left):
                    # If the user clicks outside the drawing pad, it is assumed that they want to terminate the tool
                    if get_active_window() != "Drawing Pad":
                        delete_draw_command(pad_name, f"circle {circleCount}")
                        print("\nCircle tool terminated.")
                        return

                    circleCount += 1
                    time.sleep(0.01)
                    return

                # Check if user wants to exit the line tool
                if is_mouse_button_released(mvMouseButton_Right):
                    delete_draw_command(pad_name, f"circle {circleCount}")
                    return

                # Check if user wants to exit the line tool
                if is_key_released(mvKey_Escape):
                    delete_draw_command(pad_name, f"circle {circleCount}")
                    return

                # Delete the line drawn and begin the process again till user clicks the second point or exits the tool
                delete_draw_command(pad_name, f"circle {circleCount}")

def fillCircleCheckbox():
    if get_value("Fill circle"):
        set_item_height("tool properties", height=215)
        add_spacing(count=2, parent="tool properties", name="tempSpace1")
        add_checkbox("Fill with same color", default_value=False, parent="tool properties", callback=fillSameCircleCheckbox)
        add_spacing(count=2, parent="tool properties", name="tempSpace2")
        add_color_edit4("Fill color", default_value=[0, 255, 255, 255], parent="tool properties", width=155)

    else:
        delete_item("Fill with same color")
        delete_item("tempSpace1")
        delete_item("tempSpace2")
        delete_item("Fill color")
        set_item_height("tool properties", height=135)

def fillSameCircleCheckbox():
    if get_value("Fill with same color"):
        delete_item("tempSpace2")
        delete_item("Fill color")
        set_item_height("tool properties", height=175)

    else:
        set_item_height("tool properties", height=215)
        add_spacing(count=2, parent="tool properties", name="tempSpace2")
        add_color_edit4("Fill color", default_value=[0, 255, 255, 255], parent="tool properties", width=155)