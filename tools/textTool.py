import dearpygui.dearpygui as dpg
from windows.base_window import *
from windows.layer_properties import *

import threading
import time
import tools.config

from tkinter import Tk
from tkinter.filedialog import askopenfilename

left_mouse_release_flag = 0  # Handling left mouse button clicks
esc_key_release_flag = 0  # Handling escape key button presses

dpg.setup_registries()  # Registries for mouse and keyboard press events


def set_textTool_properties():
    # Initialize all variables associated with text parameters
    global text_input, text_size, text_font, text_color
    global custom_font_button, custom_font_text_name, custom_font_text_path

    # Sets up the properties window
    with dpg.group(parent=tool_properties) as tool_properties_group:
        dpg.set_item_theme(item=tool_properties_group, theme=tool_properties_group_theme)

        text_tool_header = dpg.add_text("Text Tool")
        dpg.set_item_font(item=text_tool_header, font=bold_font)
        dpg.add_separator()

        # As soon as a change is made in these widgets, the text tool is automatically called using the tool dispatcher
        text_input = dpg.add_input_text(label="Text", default_value="Example text", width=160, height=50,
                                        multiline=False, on_enter=True, callback=textToolDispatcher)
        text_size = dpg.add_drag_int(label="Size", default_value=32, min_value=1, width=160, speed=1,
                                     callback=textToolDispatcher)
        text_color = dpg.add_color_edit(label="Color", width=160, no_tooltip=True, callback=textToolDispatcher)
        items = ["Roboto - Regular", "Roboto - Bold", "Roboto - Italic", "Custom font"]
        text_font = dpg.add_combo(items=items, label="Font", width=160, height_mode=dpg.mvComboHeight_Small,
                                  default_value="Roboto - Regular", callback=check_textFont)
        dpg.set_item_theme(item=text_font, theme=combo_theme)
        dpg.add_dummy()
        custom_font_button = dpg.add_button(label="Choose font", width=-1, show=False,
                                            callback=lambda: dpg.show_item(custom_font_file_directory))
        custom_font_text_name = dpg.add_text(default_value="Font selected: ", color=[170, 170, 170], wrap=200,
                                             show=False)
        custom_font_text_path = dpg.add_text(default_value="", color=[170, 170, 170], wrap=200, show=False)
        dpg.add_mouse_release_handler(callback=mouse_key_release_handler)
        dpg.add_key_release_handler(callback=mouse_key_release_handler)

    with dpg.file_dialog(label="SimpleDrawing - Custom Font File", directory_selector=False, show=False, modal=True,
                         callback=choose_font_file) as custom_font_file_directory:
        dpg.set_item_theme(item=custom_font_file_directory, theme=popup_theme)
        dpg.add_file_extension(".ttf", color=(255, 255, 0, 255))
        dpg.add_file_extension(".otf", color=(0, 255, 0, 255))



def mouse_key_release_handler(sender, app_data):
    # Function changes flags when a mouse or key release event occurs
    global left_mouse_release_flag, esc_key_release_flag

    if app_data == 0:
        left_mouse_release_flag = 1  # Marking flag as 1 to indicate left mouse button has been released

    elif app_data == 27:
        esc_key_release_flag = 1  # Marking flag as 1 to indicate escape key has been released


def check_textFont():
    if dpg.get_value(item=text_font) == "Custom font":
        dpg.configure_item(item=custom_font_button, show=True)
        dpg.configure_item(item=custom_font_text_name, show=True)
    else:
        dpg.configure_item(item=custom_font_button, show=False)
        dpg.configure_item(item=custom_font_text_name, show=False)

    textToolDispatcher()


def choose_font_file(sender, app_data):
    if app_data["file_name_buffer"] != ".":
        file_path = app_data["file_path_name"]
        file_name = app_data["file_name"]
        dpg.set_value(item=custom_font_text_name, value=f"Font selected: {file_name}")
        dpg.set_value(item=custom_font_text_path, value=file_path)

        textToolDispatcher()


def textToolDispatcher():
    # Function creates a new thread to run parallel with the main code
    tools.config.thread_count += 1
    text_tool_thread = threading.Thread(name="text_tool", target=start_textTool, args=(), daemon=True)
    text_tool_thread.start()


def start_textTool():
    global left_mouse_release_flag, esc_key_release_flag

    text = dpg.get_value(item=text_input)
    size = dpg.get_value(item=text_size)
    color = dpg.get_value(item=text_color)
    font_path = dpg.get_value(item=custom_font_text_path)

    if dpg.get_value(item=text_font) == "Custom font":
        if font_path:
            temp_font = dpg.add_font(file=font_path, size=size, parent=main_font_registry)
        else:
            temp_font = regular_font

    else:
        default_font = dpg.get_value(item=text_font)
        if default_font == "Roboto - Regular":
            temp_font = regular_font

        elif default_font == "Roboto - Bold":
            temp_font = bold_font

        else:
            temp_font = italic_font

    # Get what layer the user has selected in the radio button list
    # Get index of list layers from the name in radio button list
    # Use the index to find the ID from the layers_id list
    layer_id = layer_ids[(layers.index(dpg.get_value(item=active_layer)))]

    while True:

        # Check if a new thread has started and stop the function to end the old thread
        if tools.config.thread_count != 1:
            tools.config.thread_count = 1  # Reset thread count
            return

        # If the left mouse button is clicked, start drawing
        if left_mouse_release_flag == 1:
            left_mouse_release_flag = 0  # Reset the flag

            # Check if the user clicks inside the drawing area. If yes, continue, otherwise exit
            if dpg.get_active_window() == drawing_pad:
                while True:
                    # Keep track of points
                    text_position = dpg.get_plot_mouse_pos()

                    temp_text = dpg.draw_text(pos=text_position, text=text, color=color, size=size, parent=layer_id)
                    dpg.set_item_font(item=temp_text, font=temp_font)

                    if tools.config.thread_count != 1:
                        tools.config.thread_count = 1  # Reset thread count
                        dpg.delete_item(temp_text)
                        dpg.delete_item(item=temp_font)
                        return

                    # Check if the user clicks inside the drawing area. If yes, continue drawing, otherwise exit
                    if left_mouse_release_flag == 1:
                        left_mouse_release_flag = 0
                        if dpg.get_active_window() == drawing_pad:
                            break

                    elif esc_key_release_flag == 1:
                        esc_key_release_flag = 0
                        dpg.delete_item(temp_text)
                        break

                    time.sleep(0.01)
                    dpg.delete_item(temp_text)
