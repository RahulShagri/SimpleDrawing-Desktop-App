import dearpygui.dearpygui as dpg
from windows.base_window import *
from windows.layer_properties import *
from tools.get_angle_tool import get_angle
from tools.draw_dashed_line import *
from tools.draw_dotted_line import *
from tools.draw_dot_dashed_line import *

import threading
import time
import tools.config

left_mouse_flag = 0  # Handling left mouse button clicks
esc_key_flag = 0  # Handling escape key button presses
shift_key_flag = 0  # Handling shift key button presses

dpg.setup_registries()  # Registries for mouse and keyboard press events


def set_lineTool_properties():
    # Initialize all variables associated with line parameters
    global line_type, line_thickness, line_color, line_spacing, dot_radius, line_closed

    # Sets up the properties window
    with dpg.group(parent=tool_properties) as tool_properties_group:
        dpg.set_item_theme(item=tool_properties_group, theme=tool_properties_group_theme)

        line_tool_header = dpg.add_text("Line Tool")
        dpg.set_item_font(item=line_tool_header, font=bold_font)
        dpg.add_separator()


        # Adds combo to select type of line, thickness, color, spacing, and dot radius input widgets
        # As soon as a change is made in these widgets, the line tool is automatically called using the tool dispatcher
        items = ["Solid line", "Dashed line", "Dotted line", "Dot dashed line"]
        line_type = dpg.add_combo(items=items, label="Type", height_mode=dpg.mvComboHeight_Small,
                                  default_value="Solid line", callback=check_lineType)
        dpg.add_dummy()
        dpg.set_item_theme(item=line_type, theme=combo_theme)

        line_thickness = dpg.add_drag_float(label="Thickness", default_value=2, clamped=True, min_value=0.1, width=120,
                                            format="%0.01f", speed=0.1, callback=lineToolDispatcher)
        line_color = dpg.add_color_edit(label="Color", width=160, no_tooltip=True, callback=lineToolDispatcher)
        line_spacing = dpg.add_drag_float(label="Spacing", default_value=15, min_value=0.1, speed=0.1, clamped=True,
                                          format="%0.01f", show=False, width=120, callback=lineToolDispatcher)
        dot_radius = dpg.add_drag_float(label="Dot Radius", default_value=2, min_value=0.1, speed=0.1, show=False,
                                        format="%0.01f", width=120, clamped=True, callback=lineToolDispatcher)
        line_closed = dpg.add_checkbox(label="Closed", callback=lineToolDispatcher)

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


def check_lineType():
    # Check whether user wants solid type or other type of line and change parameters accordingly
    if dpg.get_value(item=line_type) == "Solid line":
        dpg.configure_item(item=line_thickness, show=True)
        dpg.configure_item(item=line_spacing, show=False)
        dpg.configure_item(item=dot_radius, show=False)

    elif dpg.get_value(item=line_type) == "Dashed line":
        dpg.configure_item(item=line_thickness, show=True)
        dpg.configure_item(item=line_spacing, show=True)
        dpg.configure_item(item=dot_radius, show=False)

    elif dpg.get_value(item=line_type) == "Dotted line":
        dpg.configure_item(item=line_thickness, show=False)
        dpg.configure_item(item=line_spacing, show=True)
        dpg.configure_item(item=dot_radius, show=True)

    elif dpg.get_value(item=line_type) == "Dot dashed line":
        dpg.configure_item(item=line_thickness, show=True)
        dpg.configure_item(item=line_spacing, show=True)
        dpg.configure_item(item=dot_radius, show=True)

    lineToolDispatcher()


def lineToolDispatcher():
    # Function creates a new thread to run parallel with the main code
    tools.config.thread_count += 1
    line_tool_thread = threading.Thread(name="line_tool", target=start_lineTool, args=(), daemon=True)
    line_tool_thread.start()


def start_lineTool():
    # Check what type of line the user wants
    if dpg.get_value(item=line_type) == "Solid line":
        start_solidLineTool()

    elif dpg.get_value(item=line_type) == "Dashed line":
        start_dashedLineTool()

    elif dpg.get_value(item=line_type) == "Dotted line":
        start_dottedLineTool()

    else:
        start_dotDashedLineTool()


def start_solidLineTool():
    global left_mouse_flag, esc_key_flag, shift_key_flag

    # Get user settings
    thickness = dpg.get_value(item=line_thickness)
    color = dpg.get_value(item=line_color)
    closed = dpg.get_value(item=line_closed)

    # Get what layer the user has selected in the radio button list
    # Get index of list layers from the name in radio button list
    # Use the index to find the ID from the layers_id list
    layer_id = layer_ids[(layers.index(dpg.get_value(item=active_layer)))]

    while True:
        line_points = []  # List of all end points of the lines drawn
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
                first_point = dpg.get_plot_mouse_pos()
                line_points.append(first_point)
                temp_line = None
                while True:
                    line_points.append(dpg.get_plot_mouse_pos())

                    if shift_key_flag == 1:
                        shift_key_flag = 0  # Reset shift key flag
                        angle = get_angle(first_point, line_points[-1])

                        if 0 <= angle <= 30:
                            line_points[-1] = [dpg.get_plot_mouse_pos()[0], first_point[1]]
                            temp_line = dpg.draw_line(p1=first_point, p2=line_points[-1], thickness=thickness,
                                                      color=color, parent=layer_id)

                        elif 30 < angle <= 60:
                            p2_y = 0

                            if (line_points[-1][1] - first_point[1]) > 0:
                                if (line_points[-1][0] - first_point[0]) > 0:
                                    p2_y = first_point[1] - (first_point[0] - line_points[-1][0])
                                else:
                                    p2_y = first_point[1] + (first_point[0] - line_points[-1][0])

                            elif (line_points[-1][1] - first_point[1]) < 0:
                                if (line_points[-1][0] - first_point[0]) > 0:
                                    p2_y = first_point[1] + (first_point[0] - line_points[-1][0])
                                else:
                                    p2_y = first_point[1] - (first_point[0] - line_points[-1][0])

                            line_points[-1] = [line_points[-1][0], p2_y]
                            temp_line = dpg.draw_line(p1=first_point, p2=line_points[-1], color=color,
                                                      thickness=thickness, parent=layer_id)

                        elif 60 < angle <= 90:
                            line_points[-1] = [first_point[0], line_points[-1][1]]
                            temp_line = dpg.draw_line(p1=first_point, p2=line_points[-1], color=color,
                                                      thickness=thickness, parent=layer_id)

                    # Draw a temporary line
                    else:
                        temp_line = dpg.draw_line(p1=first_point, p2=line_points[-1], thickness=thickness,
                                                  color=color, parent=layer_id)

                    # Check if a new thread has started and stop the function to end the old thread
                    if tools.config.thread_count != 1:
                        tools.config.thread_count = 1  # Reset thread count
                        dpg.delete_item(temp_line)
                        line_points = line_points[:-1]
                        return

                    # Check if the user clicks inside the drawing area. If yes, continue drawing, otherwise exit
                    if left_mouse_flag == 1:
                        left_mouse_flag = 0
                        if dpg.get_active_window() == drawing_pad:
                            first_point = line_points[-1]
                            continue

                        else:
                            dpg.delete_item(temp_line)
                            line_points = line_points[:-1]

                            # Check if the user wants to close the polyline. Draw if more than two points already exist
                            if closed and len(line_points) > 2:
                                dpg.draw_line(p1=line_points[0], p2=line_points[-1], thickness=thickness, color=color,
                                              parent=layer_id)

                            break

                    elif esc_key_flag == 1:
                        esc_key_flag = 0
                        dpg.delete_item(temp_line)
                        line_points = line_points[:-1]

                        # Check if the user wants to close the polyline. Draw if more than two points already exist
                        if closed and len(line_points) > 2:
                            dpg.draw_line(p1=line_points[0], p2=line_points[-1], thickness=thickness, color=color,
                                          parent=layer_id)

                        break

                    time.sleep(0.02)
                    dpg.delete_item(temp_line)
                    line_points.pop()


def start_dashedLineTool():
    global left_mouse_flag, esc_key_flag, shift_key_flag
    line_points = []  # List of all end points of the lines drawn

    # Get user settings
    thickness = dpg.get_value(item=line_thickness)
    color = dpg.get_value(item=line_color)
    spacing = dpg.get_value(item=line_spacing)
    closed = dpg.get_value(item=line_closed)

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

        # If the left mouse button is clicked, start drawing
        if left_mouse_flag == 1:
            left_mouse_flag = 0  # Reset the flag

            # Check if the user clicks inside the drawing area. If yes, continue, otherwise exit
            if dpg.get_active_window() == drawing_pad:
                # Keep track of points
                first_point = dpg.get_plot_mouse_pos()
                line_points.append(first_point)

                while True:
                    line_points.append(dpg.get_plot_mouse_pos())

                    # Check if a new thread has started and stop the function to end the old thread
                    if tools.config.thread_count != 1:
                        tools.config.thread_count = 1  # Reset thread count
                        clear_dashed_line()
                        line_points = line_points[:-1]
                        return

                    # Draw a temporary line
                    if shift_key_flag == 1:
                        shift_key_flag = 0  # Reset shift key flag
                        angle = get_angle(first_point, line_points[-1])

                        if 0 <= angle <= 30:
                            line_points[-1] = [dpg.get_plot_mouse_pos()[0], first_point[1]]
                            draw_dashed_line(p1=first_point, p2=line_points[-1], thickness=thickness, spacing=spacing,
                                             color=color, parent=layer_id)

                        elif 30 < angle <= 60:
                            p2_y = 0

                            if (line_points[-1][1] - first_point[1]) > 0:
                                if (line_points[-1][0] - first_point[0]) > 0:
                                    p2_y = first_point[1] - (first_point[0] - line_points[-1][0])
                                else:
                                    p2_y = first_point[1] + (first_point[0] - line_points[-1][0])

                            elif (line_points[-1][1] - first_point[1]) < 0:
                                if (line_points[-1][0] - first_point[0]) > 0:
                                    p2_y = first_point[1] + (first_point[0] - line_points[-1][0])
                                else:
                                    p2_y = first_point[1] - (first_point[0] - line_points[-1][0])

                            line_points[-1] = [line_points[-1][0], p2_y]
                            draw_dashed_line(p1=first_point, p2=line_points[-1], thickness=thickness, spacing=spacing,
                                             color=color, parent=layer_id)

                        elif 60 < angle <= 90:
                            line_points[-1] = [first_point[0], line_points[-1][1]]
                            draw_dashed_line(p1=first_point, p2=line_points[-1], thickness=thickness, spacing=spacing,
                                             color=color, parent=layer_id)

                    else:
                        draw_dashed_line(p1=first_point, p2=line_points[-1], thickness=thickness, color=color,
                                         spacing=spacing, parent=layer_id)

                    # Check if the user clicks inside the drawing area. If yes, continue drawing, otherwise exit
                    if left_mouse_flag == 1:
                        left_mouse_flag = 0
                        if dpg.get_active_window() == drawing_pad:
                            first_point = line_points[-1]
                            clear_dashed_line(new_line_flag=1)
                            continue

                        else:
                            clear_dashed_line()
                            line_points = line_points[:-1]

                            # Check if the user wants to close the polyline. Draw if more than two points already exist
                            if closed and len(line_points) > 2:
                                draw_dashed_line(p1=line_points[0], p2=line_points[-1], thickness=thickness,
                                                 color=color, spacing=spacing, parent=layer_id)

                            break
                    # Check if user presses esc_key_flag and end drawing
                    elif esc_key_flag == 1:
                        esc_key_flag = 0
                        clear_dashed_line()
                        line_points = line_points[:-1]

                        # Check if the user wants to close the polyline. Draw if more than two points already exist
                        if closed and len(line_points) > 2:
                            draw_dashed_line(p1=line_points[0], p2=line_points[-1], thickness=thickness, color=color,
                                             spacing=spacing, parent=layer_id)
                            clear_dashed_line(new_line_flag=1)

                        break

                    time.sleep(0.02)
                    clear_dashed_line()
                    line_points.pop()


def start_dottedLineTool():
    global left_mouse_flag, esc_key_flag, shift_key_flag
    line_points = []  # List of all end points of the lines drawn

    # Get user settings
    thickness = dpg.get_value(item=line_thickness)
    color = dpg.get_value(item=line_color)
    spacing = dpg.get_value(item=line_spacing)
    radius = dpg.get_value(item=dot_radius)
    closed = dpg.get_value(item=line_closed)

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

        # If the left mouse button is clicked, start drawing
        if left_mouse_flag == 1:
            left_mouse_flag = 0  # Reset the flag

            # Check if the user clicks inside the drawing area. If yes, continue, otherwise exit
            if dpg.get_active_window() == drawing_pad:
                # Keep track of points
                first_point = dpg.get_plot_mouse_pos()
                line_points.append(first_point)

                while True:
                    line_points.append(dpg.get_plot_mouse_pos())
                    # Draw a temporary line

                    if shift_key_flag == 1:
                        shift_key_flag = 0  # Reset shift key flag
                        angle = get_angle(first_point, line_points[-1])

                        if 0 <= angle <= 30:
                            line_points[-1] = [dpg.get_plot_mouse_pos()[0], first_point[1]]
                            draw_dotted_line(p1=first_point, p2=line_points[-1], color=color, spacing=spacing,
                                             radius=radius, parent=layer_id)

                        elif 30 < angle <= 60:
                            p2_y = 0

                            if (line_points[-1][1] - first_point[1]) > 0:
                                if (line_points[-1][0] - first_point[0]) > 0:
                                    p2_y = first_point[1] - (first_point[0] - line_points[-1][0])
                                else:
                                    p2_y = first_point[1] + (first_point[0] - line_points[-1][0])

                            elif (line_points[-1][1] - first_point[1]) < 0:
                                if (line_points[-1][0] - first_point[0]) > 0:
                                    p2_y = first_point[1] + (first_point[0] - line_points[-1][0])
                                else:
                                    p2_y = first_point[1] - (first_point[0] - line_points[-1][0])

                            line_points[-1] = [line_points[-1][0], p2_y]
                            draw_dotted_line(p1=first_point, p2=line_points[-1], color=color, spacing=spacing,
                                             radius=radius, parent=layer_id)

                        elif 60 < angle <= 90:
                            line_points[-1] = [first_point[0], line_points[-1][1]]
                            draw_dotted_line(p1=first_point, p2=line_points[-1], color=color, spacing=spacing,
                                             radius=radius, parent=layer_id)

                    else:
                        draw_dotted_line(p1=first_point, p2=line_points[-1], color=color, spacing=spacing,
                                         radius=radius, parent=layer_id)

                    # Check if a new thread has started and stop the function to end the old thread
                    if tools.config.thread_count != 1:
                        tools.config.thread_count = 1  # Reset thread count
                        clear_dotted_line()
                        line_points = line_points[:-1]
                        return

                    # Check if the user clicks inside the drawing area. If yes, continue drawing, otherwise exit
                    if left_mouse_flag == 1:
                        left_mouse_flag = 0
                        if dpg.get_active_window() == drawing_pad:
                            first_point = line_points[-1]
                            clear_dotted_line(new_line_flag=1)
                            continue

                        else:
                            clear_dotted_line()
                            line_points = line_points[:-1]

                            # Check if the user wants to close the polyline. Draw if more than two points already exist
                            if closed and len(line_points) > 2:
                                draw_dotted_line(p1=line_points[0], p2=line_points[-1],
                                                 color=color, spacing=spacing, radius=radius, parent=layer_id)

                            break
                    # Check if user presses esc_key_flag and end drawing
                    elif esc_key_flag == 1:
                        esc_key_flag = 0
                        clear_dotted_line()
                        line_points = line_points[:-1]

                        # Check if the user wants to close the polyline. Draw if more than two points already exist
                        if closed and len(line_points) > 2:
                            draw_dotted_line(p1=line_points[0], p2=line_points[-1], color=color,
                                             spacing=spacing, radius=radius, parent=layer_id)
                            clear_dotted_line(new_line_flag=1)

                        break

                    time.sleep(0.02)
                    clear_dotted_line()
                    line_points.pop()


def start_dotDashedLineTool():
    global left_mouse_flag, esc_key_flag, shift_key_flag
    line_points = []  # List of all end points of the lines drawn

    # Get user settings
    thickness = dpg.get_value(item=line_thickness)
    color = dpg.get_value(item=line_color)
    spacing = dpg.get_value(item=line_spacing)
    radius = dpg.get_value(item=dot_radius)
    closed = dpg.get_value(item=line_closed)

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

        # If the left mouse button is clicked, start drawing
        if left_mouse_flag == 1:
            left_mouse_flag = 0  # Reset the flag

            # Check if the user clicks inside the drawing area. If yes, continue, otherwise exit
            if dpg.get_active_window() == drawing_pad:
                # Keep track of points
                first_point = dpg.get_plot_mouse_pos()
                line_points.append(first_point)

                while True:
                    line_points.append(dpg.get_plot_mouse_pos())
                    # Draw a temporary line

                    if shift_key_flag == 1:
                        shift_key_flag = 0  # Reset shift key flag
                        angle = get_angle(first_point, line_points[-1])

                        if 0 <= angle <= 30:
                            line_points[-1] = [dpg.get_plot_mouse_pos()[0], first_point[1]]
                            draw_dot_dashed_line(p1=first_point, p2=line_points[-1], thickness=thickness, color=color,
                                                 spacing=spacing, radius=radius, parent=layer_id)

                        elif 30 < angle <= 60:
                            p2_y = 0

                            if (line_points[-1][1] - first_point[1]) > 0:
                                if (line_points[-1][0] - first_point[0]) > 0:
                                    p2_y = first_point[1] - (first_point[0] - line_points[-1][0])
                                else:
                                    p2_y = first_point[1] + (first_point[0] - line_points[-1][0])

                            elif (line_points[-1][1] - first_point[1]) < 0:
                                if (line_points[-1][0] - first_point[0]) > 0:
                                    p2_y = first_point[1] + (first_point[0] - line_points[-1][0])
                                else:
                                    p2_y = first_point[1] - (first_point[0] - line_points[-1][0])

                            line_points[-1] = [line_points[-1][0], p2_y]
                            draw_dot_dashed_line(p1=first_point, p2=line_points[-1], thickness=thickness, color=color,
                                                 spacing=spacing, radius=radius, parent=layer_id)

                        elif 60 < angle <= 90:
                            line_points[-1] = [first_point[0], line_points[-1][1]]
                            draw_dot_dashed_line(p1=first_point, p2=line_points[-1], thickness=thickness, color=color,
                                                 spacing=spacing, radius=radius, parent=layer_id)

                    else:
                        draw_dot_dashed_line(p1=first_point, p2=line_points[-1], thickness=thickness, color=color,
                                             spacing=spacing, radius=radius, parent=layer_id)

                    # Check if a new thread has started and stop the function to end the old thread
                    if tools.config.thread_count != 1:
                        tools.config.thread_count = 1  # Reset thread count
                        clear_dot_dashed_line()
                        line_points = line_points[:-1]
                        return

                    # Check if the user clicks inside the drawing area. If yes, continue drawing, otherwise exit
                    if left_mouse_flag == 1:
                        left_mouse_flag = 0
                        if dpg.get_active_window() == drawing_pad:
                            first_point = line_points[-1]
                            clear_dot_dashed_line(new_line_flag=1)
                            continue

                        else:
                            clear_dot_dashed_line()
                            line_points = line_points[:-1]

                            # Check if the user wants to close the polyline. Draw if more than two points already exist
                            if closed and len(line_points) > 2:
                                draw_dot_dashed_line(p1=line_points[0], p2=line_points[-1], thickness=thickness,
                                                     color=color, spacing=spacing, radius=radius, parent=layer_id)

                            break
                    # Check if user presses esc_key_flag and end drawing
                    elif esc_key_flag == 1:
                        esc_key_flag = 0
                        clear_dot_dashed_line()
                        line_points = line_points[:-1]

                        # Check if the user wants to close the polyline. Draw if more than two points already exist
                        if closed and len(line_points) > 2:
                            draw_dot_dashed_line(p1=line_points[0], p2=line_points[-1], thickness=thickness,
                                                 color=color, spacing=spacing, radius=radius, parent=layer_id)
                            clear_dot_dashed_line(new_line_flag=1)

                        break

                    time.sleep(0.02)
                    clear_dot_dashed_line()
                    line_points.pop()
