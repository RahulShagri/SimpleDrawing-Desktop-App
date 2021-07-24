import dearpygui.dearpygui as dpg
from windows.base_window import *
from windows.layer_properties import *

import threading
import time
import tools.config

left_mouse_flag = 0  # Handling left mouse button clicks
esc_key_flag = 0  # Handling escape key button presses
shift_key_flag = 0  # Handling shift key button presses

dpg.setup_registries()  # Registries for mouse and keyboard press events


def set_rectangleTool_properties():
    # Initialize all variables associated with rectangle parameters
    global line_thickness, line_color, edge_rounding, fill_color, fill_rectangle, fill_rectangle_same_color

    # Sets up the properties window
    with dpg.group(parent=tool_properties) as tool_properties_group:
        dpg.set_item_theme(item=tool_properties_group, theme=tool_properties_group_theme)

        rectangle_tool_header = dpg.add_text("Rectangle Tool")
        dpg.set_item_font(item=rectangle_tool_header, font=bold_font)
        dpg.add_separator()

        # As soon as a change is made in these widgets, the rectangle tool is automatically called using the tool dispatcher
        line_thickness = dpg.add_drag_float(label="Thickness", default_value=2, min_value=0.1, width=120, speed=0.1,
                                            format="%0.01f", clamped=True, callback=rectangleToolDispatcher)
        edge_rounding = dpg.add_drag_float(label="Rounding", default_value=0, min_value=0, width=120, speed=0.1,
                                           format="%0.01f", clamped=True, callback=rectangleToolDispatcher)
        line_color = dpg.add_color_edit(label="Color", width=160, no_tooltip=True, callback=rectangleToolDispatcher)
        fill_rectangle = dpg.add_checkbox(label="Fill rectangle", callback=check_fillRectangle)
        fill_rectangle_same_color = dpg.add_checkbox(label="Fill with same color", show=False,
                                                     callback=check_fillRectangle)
        fill_color = dpg.add_color_edit(label="Fill color", width=160, no_tooltip=True, show=False,
                                        callback=rectangleToolDispatcher)

        dpg.add_mouse_release_handler(callback=mouse_key_release_handler)
        dpg.add_key_release_handler(callback=mouse_key_release_handler)
        dpg.add_key_down_handler(callback=mouse_key_down_handler)


def mouse_key_release_handler(sender, app_data):
    # Function changes flags when a mouse or key release event occurs
    global left_mouse_flag, esc_key_flag

    if app_data == 0:
        left_mouse_flag = 1  # Marking flag as 1 to indicate left mouse button has been released

    elif app_data == 27:
        esc_key_flag = 1  # Marking flag as 1 to indicate escape key has been released


def mouse_key_down_handler(sender, app_data):
    # Function changes flags when a mouse or key down event occurs
    global shift_key_flag
    if app_data[0] == 16:
        shift_key_flag = 1  # Marking flag as 1 to indicate shift key has been released


def check_fillRectangle():
    global fill_rectangle, fill_color, fill_rectangle_same_color

    if dpg.get_value(item=fill_rectangle):
        dpg.configure_item(item=fill_rectangle_same_color, show=True)
        if dpg.get_value(item=fill_rectangle_same_color):
            dpg.configure_item(item=fill_color, show=False)
        else:
            dpg.configure_item(item=fill_color, show=True)
    else:
        dpg.configure_item(item=fill_rectangle_same_color, show=False)
        dpg.configure_item(item=fill_color, show=False)

    rectangleToolDispatcher()

def rectangleToolDispatcher():
    # Function creates a new thread to run parallel with the main code
    tools.config.thread_count += 1
    rectangle_tool_thread = threading.Thread(name="rectangle_tool", target=start_rectangleTool, args=(), daemon=True)
    rectangle_tool_thread.start()


def start_rectangleTool():
    global left_mouse_flag, esc_key_flag, shift_key_flag

    # Get user settings
    thickness = dpg.get_value(item=line_thickness)
    color = dpg.get_value(item=line_color)
    rounding = dpg.get_value(item=edge_rounding)

    if dpg.get_value(item=fill_rectangle):
        if dpg.get_value(item=fill_rectangle_same_color):
            fill = color
        else:
            fill = dpg.get_value(item=fill_color)
    else:
        fill = [0, 0, 0, 0]

    # Get what layer the user has selected in the radio button list
    # Get index of list layers from the name in radio button list
    # Use the index to find the ID from the layers_id list
    layer_id = layer_ids[(layers.index(dpg.get_value(item=active_layer)))]

    while True:
        end_points = []  # List of end points of the rectangle

        # Check if a new thread has started and stop the function to end the old thread
        if tools.config.thread_count != 1:
            tools.config.thread_count = 1  # Reset thread count
            return

        # If the left mouse button is clicked, start drawing
        if left_mouse_flag == 1:
            left_mouse_flag = 0  # Reset the flag
            # Check if the user clicks inside the drawing area. If yes, continue, otherwise exit
            if dpg.get_active_window() == drawing_pad:
                # Keep track of points
                end_points.append(dpg.get_plot_mouse_pos())

                while True:
                    end_points.append(dpg.get_plot_mouse_pos())
                    # Check which quadrant the second point is in, and change the end points accordingly because of
                    # imGui bug
                    # Holding down the shift key will draw a square
                    if shift_key_flag == 1:
                        shift_key_flag = 0
                        if end_points[1][0] < end_points[0][0]:
                            # Check if in second quadrant
                            if end_points[1][1] > end_points[0][1]:
                                first_point = end_points[0]
                                second_point = [end_points[0][0] - (end_points[1][1] - end_points[0][1]),
                                                end_points[1][1]]

                                temp_rectangle = dpg.draw_rectangle(pmin=first_point, pmax=second_point,
                                                                    thickness=thickness, color=color,
                                                                    rounding=rounding, fill=fill, parent=layer_id)
                            # Check if in third quadrant
                            else:
                                first_point = [end_points[0][0], end_points[1][1]]
                                second_point = [end_points[0][0] - (end_points[0][1] - end_points[1][1]),
                                                end_points[0][1]]

                                temp_rectangle = dpg.draw_rectangle(pmin=first_point, pmax=second_point,
                                                                    thickness=thickness, color=color,
                                                                    rounding=rounding, fill=fill, parent=layer_id)
                        # Check if in first quadrant
                        elif end_points[1][1] > end_points[0][1]:
                            first_point = [end_points[0][0] + (end_points[1][1] - end_points[0][1]),
                                           end_points[0][1]]
                            second_point = [end_points[0][0], end_points[1][1]]

                            temp_rectangle = dpg.draw_rectangle(pmin=first_point, pmax=second_point,
                                                                thickness=thickness, color=color,
                                                                rounding=rounding, fill=fill, parent=layer_id)


                        # Check if in fourth quadrant
                        else:
                            first_point = [end_points[0][0] + (end_points[0][1] - end_points[1][1]),
                                           end_points[1][1]]
                            second_point = end_points[0]

                            temp_rectangle = dpg.draw_rectangle(pmin=first_point, pmax=second_point,
                                                                thickness=thickness, color=color,
                                                                rounding=rounding, fill=fill, parent=layer_id)


                        # For creating rectangles
                    else:
                        if end_points[1][0] < end_points[0][0]:
                            # Check if in second quadrant
                            if end_points[1][1] > end_points[0][1]:
                                first_point = end_points[0]
                                second_point = end_points[1]

                                temp_rectangle = dpg.draw_rectangle(pmin=first_point, pmax=second_point,
                                                                    thickness=thickness, color=color,
                                                                    rounding=rounding, fill=fill, parent=layer_id)

                            # Check if in third quadrant
                            else:
                                first_point = [end_points[0][0], end_points[1][1]]
                                second_point = [end_points[1][0], end_points[0][1]]

                                temp_rectangle = dpg.draw_rectangle(pmin=first_point, pmax=second_point,
                                                                    thickness=thickness, color=color,
                                                                    rounding=rounding, fill=fill, parent=layer_id)
                        # Check if in first quadrant
                        elif end_points[1][1] > end_points[0][1]:
                            first_point = [end_points[1][0], end_points[0][1]]
                            second_point = [end_points[0][0], end_points[1][1]]

                            temp_rectangle = dpg.draw_rectangle(pmin=first_point, pmax=second_point,
                                                                thickness=thickness, color=color,
                                                                rounding=rounding, fill=fill, parent=layer_id)

                        # Check if in fourth quadrant
                        else:
                            first_point = end_points[1]
                            second_point = end_points[0]

                            temp_rectangle = dpg.draw_rectangle(pmin=first_point, pmax=second_point,
                                                                thickness=thickness, color=color,
                                                                rounding=rounding, fill=fill, parent=layer_id)

                    # Check if a new thread has started and stop the function to end the old thread
                    if tools.config.thread_count != 1:
                        tools.config.thread_count = 1  # Reset thread count
                        dpg.delete_item(temp_rectangle)
                        return

                    # Check if the user clicks inside the drawing area. If yes, continue drawing, otherwise exit
                    if left_mouse_flag == 1:
                        left_mouse_flag = 0
                        if dpg.get_active_window() == drawing_pad:
                            break

                    elif esc_key_flag == 1:
                        esc_key_flag = 0
                        dpg.delete_item(temp_rectangle)
                        break

                    time.sleep(0.02)
                    end_points.pop()
                    dpg.delete_item(temp_rectangle)