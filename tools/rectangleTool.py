from dearpygui.core import *
from dearpygui.simple import *
import time

rectangleCount = 0


def rectangleTool(pad_name, lineColor, lineThickness, edgeRounding, fillRectangle):
    print("\nRectangle tool initiated.")

    global rectangleCount  # Keeping a track of the number of rectangles

    time.sleep(0.1)

    while True:
        # Begin drawing when left mouse button is released
        if is_mouse_button_released(mvMouseButton_Left):

            # If mouse is clicked outside the Drawing Pad, exit the tool.
            if get_active_window() != "Drawing Pad":
                print("\nRectangle tool terminated.")
                return

            # Continue of clicked on the drawing pad
            mouse_position = get_drawing_mouse_pos()
            time.sleep(0.01)

            while True:
                # Draw line
                if get_drawing_mouse_pos()[0] < mouse_position[0]:
                    # Check if in second quadrant
                    if get_drawing_mouse_pos()[1] < mouse_position[1]:
                        first_point = get_drawing_mouse_pos()
                        second_point = mouse_position
                        draw_rectangle(pad_name, pmin=first_point, pmax=second_point, color=lineColor,
                                       thickness=lineThickness, rounding=edgeRounding, fill=fillRectangle,
                                       tag=f"rectangle {rectangleCount}")
                    # Check if in third quadrant
                    else:
                        first_point = [get_drawing_mouse_pos()[0], mouse_position[1]]
                        second_point = [mouse_position[0], get_drawing_mouse_pos()[1]]
                        draw_rectangle(pad_name, pmin=first_point, pmax=second_point, color=lineColor,
                                       thickness=lineThickness, rounding=edgeRounding, fill=fillRectangle,
                                       tag=f"rectangle {rectangleCount}")
                # Check if in first quadrant
                elif get_drawing_mouse_pos()[1] < mouse_position[1]:
                    first_point = [mouse_position[0], get_drawing_mouse_pos()[1]]
                    second_point = [get_drawing_mouse_pos()[0], mouse_position[1]]
                    draw_rectangle(pad_name, pmin=first_point, pmax=second_point, color=lineColor,
                                   thickness=lineThickness, rounding=edgeRounding, fill=fillRectangle,
                                   tag=f"rectangle {rectangleCount}")
                # Check if in fourth quadrant
                else:
                    draw_rectangle(pad_name, pmin=mouse_position, pmax=get_drawing_mouse_pos(), color=lineColor,
                                   thickness=lineThickness, rounding=edgeRounding, fill=fillRectangle,
                                   tag=f"rectangle {rectangleCount}")
                time.sleep(0.01)
                line_flag = 1

                # Check if user wants to select the second point of the line
                if is_mouse_button_released(mvMouseButton_Left):
                    # If the user clicks outside the drawing pad, it is assumed that they want to terminate the tool
                    if get_active_window() != "Drawing Pad":
                        delete_draw_command(pad_name, f"rectangle {rectangleCount}")
                        print("\nRectangle tool terminated.")
                        return

                    rectangleCount += 1
                    time.sleep(0.01)
                    return

                # Check if user wants to exit the line tool
                if is_mouse_button_released(mvMouseButton_Right):
                    delete_draw_command(pad_name, f"rectangle {rectangleCount}")
                    return

                # Check if user wants to exit the line tool
                if is_key_released(mvKey_Escape):
                    delete_draw_command(pad_name, f"rectangle {rectangleCount}")
                    return

                # Delete the line drawn and begin the process again till user clicks the second point or exits the tool
                delete_draw_command(pad_name, f"rectangle {rectangleCount}")


def fillRectangleCheckbox():
    if get_value("Fill rectangle"):
        set_item_height("tool properties", height=255)
        add_spacing(count=2, parent="tool properties", name="tempSpace1")
        add_checkbox("Fill with same color", default_value=False, parent="tool properties",
                     callback=fillRectangleSameCheckbox)
        add_spacing(count=2, parent="tool properties", name="tempSpace2")
        add_color_edit4("Fill color", default_value=[0, 255, 255, 255], parent="tool properties", width=155)

    else:
        delete_item("Fill with same color")
        delete_item("tempSpace1")
        delete_item("tempSpace2")
        delete_item("Fill color")
        set_item_height("tool properties", height=175)


def fillRectangleSameCheckbox():
    if get_value("Fill with same color"):
        delete_item("tempSpace2")
        delete_item("Fill color")
        set_item_height("tool properties", height=215)

    else:
        set_item_height("tool properties", height=255)
        add_spacing(count=2, parent="tool properties", name="tempSpace2")
        add_color_edit4("Fill color", default_value=[0, 255, 255, 255], parent="tool properties", width=155)
