import dearpygui.dearpygui as dpg
from windows.base_window import *
from windows.layer_properties import *

import threading
import time
import math
import tools.config

left_mouse_flag = 0  # Handling left mouse button clicks
esc_key_flag = 0  # Handling escape key button presses

dpg.setup_registries()  # Registries for mouse and keyboard press events


def set_ellipseTool_properties():
    # Initialize all variables associated with ellipse parameters
    global line_thickness, line_color, line_segments, fill_color, fill_ellipse, fill_ellipse_same_color

    # Sets up the properties window
    with dpg.group(parent=tool_properties) as tool_properties_group:
        dpg.set_item_theme(item=tool_properties_group, theme=tool_properties_group_theme)

        ellipse_tool_header = dpg.add_text("Ellipse Tool")
        dpg.set_item_font(item=ellipse_tool_header, font=bold_font)
        dpg.add_separator()

        # As soon as a change is made in these widgets, the ellipse tool is automatically called using the tool dispatcher
        line_thickness = dpg.add_drag_float(label="Thickness", default_value=2, min_value=0.1, width=120, speed=0.1,
                                            format="%0.01f", callback=ellipseToolDispatcher)
        line_segments = dpg.add_drag_int(label="Segments", default_value=32, min_value=4, width=120, speed=1,
                                         callback=ellipseToolDispatcher)
        line_color = dpg.add_color_edit(label="Color", width=160, no_tooltip=True, callback=ellipseToolDispatcher)
        fill_ellipse = dpg.add_checkbox(label="Fill Ellipse", callback=check_fillEllipse)
        fill_ellipse_same_color = dpg.add_checkbox(label="Fill with same color", show=False,
                                                  callback=check_fillEllipse)
        fill_color = dpg.add_color_edit(label="Fill color", width=160, no_tooltip=True, show=False,
                                        callback=ellipseToolDispatcher)

        dpg.add_mouse_release_handler(callback=mouse_key_release_handler)
        dpg.add_key_release_handler(callback=mouse_key_release_handler)


def mouse_key_release_handler(sender, app_data):
    # Function changes flags when a mouse or key release event occurs
    global left_mouse_flag, esc_key_flag

    if app_data == 0:
        left_mouse_flag = 1  # Marking flag as 1 to indicate left mouse button has been released

    elif app_data == 27:
        esc_key_flag = 1  # Marking flag as 1 to indicate escape key has been released


def check_fillEllipse():
    global fill_ellipse, fill_color, fill_ellipse_same_color

    if dpg.get_value(item=fill_ellipse):
        dpg.configure_item(item=fill_ellipse_same_color, show=True)
        if dpg.get_value(item=fill_ellipse_same_color):
            dpg.configure_item(item=fill_color, show=False)
        else:
            dpg.configure_item(item=fill_color, show=True)
    else:
        dpg.configure_item(item=fill_ellipse_same_color, show=False)
        dpg.configure_item(item=fill_color, show=False)

    ellipseToolDispatcher()


def ellipseToolDispatcher():
    # Function creates a new thread to run parallel with the main code
    tools.config.thread_count += 1
    ellipse_tool_thread = threading.Thread(name="ellipse_tool", target=start_ellipseTool, args=(), daemon=True)
    ellipse_tool_thread.start()


def start_ellipseTool():
    global left_mouse_flag, esc_key_flag, shift_key_flag

    # Get user settings
    thickness = dpg.get_value(item=line_thickness)
    color = dpg.get_value(item=line_color)
    segments = dpg.get_value(item=line_segments)

    if dpg.get_value(item=fill_ellipse):
        if dpg.get_value(item=fill_ellipse_same_color):
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
        if left_mouse_flag == 1:
            left_mouse_flag = 0  # Reset the flag
            # Check if the user clicks inside the drawing area. If yes, continue, otherwise exit
            if dpg.get_active_window() == drawing_pad:
                # Record the first point selected
                end_points.append(dpg.get_plot_mouse_pos())

                while True:
                    end_points.append(dpg.get_plot_mouse_pos())  # Record the second point

                    temp_ellipse = dpg.draw_ellipse(pmin=end_points[0], pmax=end_points[1], color=color,
                                                    segments=segments, thickness=thickness, fill=fill, parent=layer_id)

                    # Check if a new thread has started and stop the function to end the old thread
                    if tools.config.thread_count != 1:
                        tools.config.thread_count = 1  # Reset thread count
                        dpg.delete_item(temp_ellipse)
                        return

                    # Check if the user clicks inside the drawing area. If yes, continue drawing, otherwise exit
                    if left_mouse_flag == 1:
                        left_mouse_flag = 0
                        if dpg.get_active_window() == drawing_pad:
                            break

                    elif esc_key_flag == 1:
                        esc_key_flag = 0
                        dpg.delete_item(temp_ellipse)
                        break

                    time.sleep(0.01)
                    end_points.pop()
                    dpg.delete_item(temp_ellipse)
