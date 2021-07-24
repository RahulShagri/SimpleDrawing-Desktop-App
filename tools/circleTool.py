import dearpygui.dearpygui as dpg
from windows.base_window import *
from windows.layer_properties import *

import threading
import time
import math
import tools.config

left_mouse_release_flag = 0  # Handling left mouse button clicks
esc_key_release_flag = 0  # Handling escape key button presses

dpg.setup_registries()  # Registries for mouse and keyboard press events


def set_circleTool_properties():
    # Initialize all variables associated with circle parameters
    global line_thickness, line_segments, use_segments, line_color, fill_color, fill_circle, fill_circle_same_color

    # Sets up the properties window
    with dpg.group(parent=tool_properties) as tool_properties_group:
        dpg.set_item_theme(item=tool_properties_group, theme=tool_properties_group_theme)

        circle_tool_header = dpg.add_text("Circle Tool")
        dpg.set_item_font(item=circle_tool_header, font=bold_font)
        dpg.add_separator()

        # As soon as a change is made in these widgets, the circle tool is automatically called using the tool dispatcher
        line_thickness = dpg.add_drag_float(label="Thickness", default_value=2, min_value=0.1, width=120, speed=0.1,
                                            format="%0.01f", clamped=True, callback=circleToolDispatcher)
        use_segments = dpg.add_checkbox(label="Use line segments", callback=check_segments)
        line_segments =  dpg.add_drag_int(label="Segments", default_value=32, min_value=4, width=120, speed=1,
                                          clamped=True, show=False, callback=circleToolDispatcher)
        line_color = dpg.add_color_edit(label="Color", width=160, no_tooltip=True, callback=circleToolDispatcher)
        fill_circle = dpg.add_checkbox(label="Fill Circle", callback=check_fillCircle)
        fill_circle_same_color = dpg.add_checkbox(label="Fill with same color", show=False,
                                                  callback=check_fillCircle)
        fill_color = dpg.add_color_edit(label="Fill color", width=160, no_tooltip=True, show=False,
                                        callback=circleToolDispatcher)

        dpg.add_mouse_release_handler(callback=mouse_key_release_handler)
        dpg.add_key_release_handler(callback=mouse_key_release_handler)


def mouse_key_release_handler(sender, app_data):
    # Function changes flags when a mouse or key release event occurs
    global left_mouse_release_flag, esc_key_release_flag

    if app_data == 0:
        left_mouse_release_flag = 1  # Marking flag as 1 to indicate left mouse button has been released

    elif app_data == 27:
        esc_key_release_flag = 1  # Marking flag as 1 to indicate escape key has been released


def check_fillCircle():
    global fill_circle, fill_color, fill_circle_same_color

    if dpg.get_value(item=fill_circle):
        dpg.configure_item(item=fill_circle_same_color, show=True)
        if dpg.get_value(item=fill_circle_same_color):
            dpg.configure_item(item=fill_color, show=False)
        else:
            dpg.configure_item(item=fill_color, show=True)
    else:
        dpg.configure_item(item=fill_circle_same_color, show=False)
        dpg.configure_item(item=fill_color, show=False)

    circleToolDispatcher()


def check_segments():
    global use_segments

    if dpg.get_value(use_segments):
        dpg.configure_item(item=line_segments, show=True)

    else:
        dpg.configure_item(item=line_segments, show=False)

    circleToolDispatcher()

def circleToolDispatcher():
    # Function creates a new thread to run parallel with the main code
    tools.config.thread_count += 1
    circle_tool_thread = threading.Thread(name="circle_tool", target=start_circleTool, args=(), daemon=True)
    circle_tool_thread.start()

def start_circleTool():
    global left_mouse_release_flag, esc_key_release_flag, shift_key_flag

    # Get user settings
    thickness = dpg.get_value(item=line_thickness)
    color = dpg.get_value(item=line_color)

    if dpg.get_value(use_segments):
        segments = dpg.get_value(item=line_segments)

    else:
        segments = 0

    if dpg.get_value(item=fill_circle):
        if dpg.get_value(item=fill_circle_same_color):
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
        end_points = []  # List of centre and radius point

        # Check if a new thread has started and stop the function to end the old thread
        if tools.config.thread_count != 1:
            tools.config.thread_count = 1  # Reset thread count
            return

        # If the left mouse button is clicked, start drawing
        if left_mouse_release_flag == 1:
            left_mouse_release_flag = 0  # Reset the flag
            # Check if the user clicks inside the drawing area. If yes, continue, otherwise exit
            if dpg.get_active_window() == drawing_pad:
                # Record the centre
                end_points.append(dpg.get_plot_mouse_pos())

                while True:
                    end_points.append(dpg.get_plot_mouse_pos())  # Record the radius point

                    # Calculate distance between centre and the radius point to get the radius
                    radius = math.sqrt(math.pow(end_points[0][0] - end_points[1][0], 2) +
                                       math.pow(end_points[0][1] - end_points[1][1], 2))

                    temp_circle = dpg.draw_circle(center=end_points[0], radius=radius, color=color, thickness=thickness,
                                                  fill=fill, parent=layer_id, segments=segments)

                    # Check if a new thread has started and stop the function to end the old thread
                    if tools.config.thread_count != 1:
                        tools.config.thread_count = 1  # Reset thread count
                        dpg.delete_item(temp_circle)
                        return

                    # Check if the user clicks inside the drawing area. If yes, continue drawing, otherwise exit
                    if left_mouse_release_flag == 1:
                        left_mouse_release_flag = 0
                        if dpg.get_active_window() == drawing_pad:
                            break

                    elif esc_key_release_flag == 1:
                        esc_key_release_flag = 0
                        dpg.delete_item(temp_circle)
                        break

                    time.sleep(0.01)
                    end_points.pop()
                    dpg.delete_item(temp_circle)
