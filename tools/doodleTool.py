import dearpygui.dearpygui as dpg
from windows.base_window import *
from windows.layer_properties import *
from tools.draw_dot_dashed_line import *

import threading
import time
import tools.config

left_mouse_click_flag = 0  # Handling left mouse button clicks
left_mouse_release_flag = 0  # Handling left mouse button release
esc_key_release_flag = 0  # Handling escape key release

dpg.setup_registries()  # Registries for mouse and keyboard press events


def set_doodleTool_properties():
    # Initialize all variables associated with line parameters
    global line_thickness, line_color

    # Sets up the properties window
    with dpg.group(parent=tool_properties) as tool_properties_group:
        dpg.set_item_theme(item=tool_properties_group, theme=tool_properties_group_theme)

        doodle_tool_header = dpg.add_text("Doodle Tool")
        dpg.set_item_font(item=doodle_tool_header, font=bold_font)
        dpg.add_separator()

        # As soon as a change is made in these widgets, the doodle tool is automatically called using the tool dispatcher
        line_thickness = dpg.add_drag_float(label="Thickness", default_value=2, clamped=True, min_value=0.1, width=120,
                                            format="%0.01f", speed=0.1, callback=doodleToolDispatcher)
        line_color = dpg.add_color_edit(label="Color", width=160, no_tooltip=True, callback=doodleToolDispatcher)

        dpg.add_mouse_click_handler(callback=mouse_key_click_handler)
        dpg.add_mouse_release_handler(callback=mouse_key_release_handler)
        dpg.add_key_release_handler(callback=mouse_key_release_handler)


def mouse_key_click_handler(sender, app_data):
    # Function changes flags when a mouse or key click event occurs
    global left_mouse_click_flag

    if app_data == 0:
        left_mouse_click_flag = 1


def mouse_key_release_handler(sender, app_data):
    # Function changes flags when a mouse or key release event occurs
    global left_mouse_release_flag, esc_key_release_flag

    if app_data == 0:
        left_mouse_release_flag = 1  # Marking flag as 1 to indicate left mouse button has been released

    elif app_data == 27:
        esc_key_release_flag = 1  # Marking flag as 1 to indicate escape key has been released


def doodleToolDispatcher():
    # Function creates a new thread to run parallel with the main code
    tools.config.thread_count += 1
    doodle_tool_thread = threading.Thread(name="line_tool", target=start_doodleTool, args=(), daemon=True)
    doodle_tool_thread.start()


def start_doodleTool():
    global left_mouse_click_flag, left_mouse_release_flag, esc_key_release_flag

    # Get user settings
    thickness = dpg.get_value(item=line_thickness)
    color = dpg.get_value(item=line_color)

    # Get what layer the user has selected in the radio button list
    # Get index of list layers from the name in radio button list
    # Use the index to find the ID from the layers_id list
    layer_id = layer_ids[(layers.index(dpg.get_value(item=active_layer)))]

    while True:
        line_points = []  # Reset list of points
        # Check if a new thread has started and stop the function to end the old thread
        if tools.config.thread_count != 1:
            tools.config.thread_count = 1  # Reset thread count
            return

        while True:
            # Check if a new thread has started and stop the function to end the old thread
            if tools.config.thread_count != 1:
                tools.config.thread_count = 1  # Reset thread count
                return

            if left_mouse_click_flag:
                if dpg.get_active_window() == drawing_pad:
                    if not line_points:
                        line_points.append(dpg.get_plot_mouse_pos())

                    if dpg.get_plot_mouse_pos() != line_points[-1]:
                        line_points.append(dpg.get_plot_mouse_pos())

                        temp_line = dpg.draw_polyline(points=line_points, thickness=thickness, color=color,
                                                      parent=layer_id)

                        time.sleep(0.02)
                        dpg.delete_item(item=temp_line)

                    else:
                        temp_line = dpg.draw_polyline(points=line_points, thickness=thickness, color=color,
                                                      parent=layer_id)

                        time.sleep(0.02)
                        dpg.delete_item(item=temp_line)

            if esc_key_release_flag == 1:
                esc_key_release_flag = 0
                left_mouse_click_flag = 0
                left_mouse_release_flag = 0

                break

            if left_mouse_release_flag:
                left_mouse_click_flag = 0
                left_mouse_release_flag = 0

                dpg.draw_polyline(points=line_points, thickness=thickness, color=color, parent=layer_id)
                break
