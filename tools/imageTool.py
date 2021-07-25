import dearpygui.dearpygui as dpg
from windows.base_window import *
from windows.layer_properties import *

import threading
import time
import tools.config

left_mouse_release_flag = 0  # Handling left mouse button release
esc_key_release_flag = 0  # Handling escape key button presses
shift_key_down_flag = 0  # Handling shift key button presses

dpg.setup_registries()  # Registries for mouse and keyboard press events


def set_imageTool_properties():
    # Initialize all variables associated with image parameters
    global image_file_path_text, image_file_name_text, image_tool_texture_registry, tool_properties_group
    global image_color_filter_checkbox, image_color_filter, image_opacity
    global thumbnail_separator, image_thumbnail

    blank_width, blank_height, blank_channel, blank_data = dpg.load_image("icons/blank_image.png")

    with dpg.texture_registry() as image_tool_texture_registry:

        blank_image = dpg.add_static_texture(blank_width, blank_height, blank_data)

    # Sets up the properties window
    with dpg.group(parent=tool_properties) as tool_properties_group:
        dpg.set_item_theme(item=tool_properties_group, theme=tool_properties_group_theme)

        image_tool_header = dpg.add_text("Image Tool")
        dpg.set_item_font(item=image_tool_header, font=bold_font)
        dpg.add_separator()

        dpg.add_button(label="Select image", width=-1, callback=lambda: dpg.show_item(custom_image_file_directory))
        image_color_filter_checkbox = dpg.add_checkbox(label="Add color filter", callback=check_image_color_filter)
        image_color_filter = dpg.add_color_edit(label="Color filter", width=140, no_tooltip=True, no_alpha=True,
                                                show=False, default_value=[255,255,255,255],
                                                callback=imageToolDispatcher)
        image_opacity = dpg.add_drag_int(label="Opacity", default_value=100, clamped=True, min_value=0, max_value=100,
                                               width=140, format="%f%%", callback=imageToolDispatcher)
        dpg.add_text(default_value="File Name: ")
        dpg.add_same_line()
        image_file_name_text = dpg.add_text(default_value="", color=[0, 255, 0], wrap=200)
        dpg.add_text(default_value="File Path: ")
        dpg.add_same_line()
        image_file_path_text = dpg.add_text(default_value="", color=[0, 255, 0], wrap=200)

        thumbnail_separator = dpg.add_separator(show=False)
        image_thumbnail = dpg.add_image(texture_id=blank_image, width=200, height=200, show=False)

        dpg.add_mouse_release_handler(callback=mouse_key_release_handler)
        dpg.add_key_release_handler(callback=mouse_key_release_handler)
        dpg.add_key_down_handler(callback=mouse_key_down_handler)

    with dpg.file_dialog(label="SimpleDrawing - Select File", directory_selector=False, show=False, modal=True,
                         callback=choose_image_file) as custom_image_file_directory:
        dpg.set_item_theme(item=custom_image_file_directory, theme=popup_theme)
        dpg.add_file_extension(".png", color=(0, 255, 0, 255))
        dpg.add_file_extension(".jpeg", color=(0, 255, 0, 255))
        dpg.add_file_extension(".jpg", color=(0, 255, 0, 255))
        dpg.add_file_extension(".*", color=(255, 255, 255, 255))


def mouse_key_release_handler(sender, app_data):
    # Function changes flags when a mouse or key release event occurs
    global left_mouse_release_flag, esc_key_release_flag

    if app_data == 0:
        left_mouse_release_flag = 1  # Marking flag as 1 to indicate left mouse button has been released

    elif app_data == 27:
        esc_key_release_flag = 1  # Marking flag as 1 to indicate escape key has been released


def mouse_key_down_handler(sender, app_data):
    # Function changes flags when a mouse or key down event occurs
    global shift_key_down_flag
    if app_data[0] == 16:
        shift_key_down_flag = 1  # Marking flag as 1 to indicate shift key has been released


def check_image_color_filter():
    if dpg.get_value(item=image_color_filter_checkbox):
        dpg.configure_item(item=image_color_filter, show=True)
    else:
        dpg.configure_item(item=image_color_filter, default_value=[255, 255, 255, 255], show=False)

    imageToolDispatcher()


def choose_image_file(sender, app_data):
    global image_tool_texture_registry, image_thumbnail, thumbnail_separator

    if app_data["file_name_buffer"] != ".":
        file_path = app_data["file_path_name"]
        file_name = app_data["file_name"]
        dpg.set_value(item=image_file_name_text, value=file_name)
        dpg.set_value(item=image_file_path_text, value=file_path)

        if dpg.get_value(item=image_file_path_text):
            image_width, image_height, image_channels, image_data = dpg.load_image(dpg.get_value(item=image_file_path_text))
            aspect_ratio = image_width/image_height
            temp_static_image = dpg.add_static_texture(image_width, image_height, image_data, parent=image_tool_texture_registry)

            dpg.configure_item(item=thumbnail_separator, show=True)

            if dpg.does_item_exist(item=image_thumbnail):
                dpg.delete_item(item=image_thumbnail)
                image_thumbnail = dpg.add_image(texture_id=temp_static_image, width=200, height=int(200/aspect_ratio),
                                                parent=tool_properties_group)

        imageToolDispatcher()


def imageToolDispatcher():
    # Function creates a new thread to run parallel with the main code
    tools.config.thread_count += 1
    image_tool_thread = threading.Thread(name="image_tool", target=start_imageTool, args=(), daemon=True)
    image_tool_thread.start()


def start_imageTool():
    global image_tool_texture_registry, image_thumbnail, thumbnail_separator
    global left_mouse_release_flag, shift_key_down_flag, esc_key_release_flag

    # Get user settings for color filter and opacity and make a complete list
    color_filter = dpg.get_value(item=image_color_filter)
    opacity = ((dpg.get_value(item=image_opacity))/100)*255  # Calculate percentage of alpha
    color = color_filter
    color.pop()
    color.append(opacity)

    # Get what layer the user has selected in the radio button list
    # Get index of list layers from the name in radio button list
    # Use the index to find the ID from the layers_id list
    layer_id = layer_ids[(layers.index(dpg.get_value(item=active_layer)))]

    while True:
        # Check if a new thread has started and stop the function to end the old thread
        if tools.config.thread_count != 1:
            tools.config.thread_count = 1  # Reset thread count
            return

        if dpg.get_value(item=image_file_path_text):
            image_width, image_height, image_channels, image_data = dpg.load_image(dpg.get_value(item=image_file_path_text))
            aspect_ratio = image_width/image_height
            temp_static_image = dpg.add_static_texture(image_width, image_height, image_data, parent=image_tool_texture_registry)

        else:
            continue

        # Begin drawing when left mouse button is released
        if left_mouse_release_flag == 1:
            left_mouse_release_flag = 0
            # If mouse is clicked outside the Drawing Pad, exit the tool.
            if dpg.get_active_window() == drawing_pad:
                # Continue if clicked on the drawing pad
                end_points = [dpg.get_plot_mouse_pos()]

                while True:
                    end_points.append(dpg.get_plot_mouse_pos())

                    if shift_key_down_flag == 1:
                        shift_key_down_flag = 0
                        if end_points[1][0] < end_points[0][0]:
                            # Check if in second quadrant
                            if end_points[1][1] > end_points[0][1]:
                                first_point = end_points[0]
                                width = aspect_ratio * (end_points[0][1] - end_points[1][1])
                                second_point = [end_points[0][0] + width, end_points[1][1]]
                                temp_image = dpg.draw_image(pmin=first_point, pmax=second_point,
                                                            texture_id=temp_static_image, color=color, parent=layer_id)

                            # Check if in third quadrant
                            else:
                                first_point = end_points[0]
                                width = aspect_ratio * (end_points[1][1] - end_points[0][1])
                                second_point = [end_points[0][0] + width, end_points[1][1]]
                                temp_image = dpg.draw_image(pmin=first_point, pmax=second_point,
                                                            texture_id=temp_static_image, color=color, parent=layer_id)

                        # Check if in first quadrant
                        elif end_points[1][1] > end_points[0][1]:
                            first_point = end_points[0]
                            width = aspect_ratio * (end_points[0][1] - end_points[1][1])
                            second_point = [end_points[0][0] - width, end_points[1][1]]
                            temp_image = dpg.draw_image(pmin=first_point, pmax=second_point,
                                                        texture_id=temp_static_image, color=color, parent=layer_id)

                        # Check if in fourth quadrant
                        else:
                            first_point = end_points[0]
                            width = aspect_ratio * (end_points[1][1] - end_points[0][1])
                            second_point = [end_points[0][0] - width, end_points[1][1]]
                            temp_image = dpg.draw_image(pmin=first_point, pmax=second_point,
                                                        texture_id=temp_static_image, color=color, parent=layer_id)

                    else:
                        first_point = end_points[0]
                        second_point = end_points[1]
                        temp_image = dpg.draw_image(pmin=first_point, pmax=second_point,
                                                    texture_id=temp_static_image, color=color, parent=layer_id)

                    # Check if user wants to select the second point of the line
                    if left_mouse_release_flag == 1:
                        left_mouse_release_flag = 0
                        # If the user clicks outside the drawing pad, it is assumed that they want to terminate the tool
                        if dpg.get_active_window() == drawing_pad:
                            break

                    # Check if user wants to exit the line tool
                    if esc_key_release_flag == 1:
                        esc_key_release_flag = 0
                        dpg.delete_item(item=temp_image)
                        break

                    # Delete the line drawn and begin the process again till user clicks the second point or exits the tool
                    time.sleep(0.02)
                    end_points.pop()
                    dpg.delete_item(item=temp_image)