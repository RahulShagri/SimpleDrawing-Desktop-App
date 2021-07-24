# Shows welcome window to user
import dearpygui.dearpygui as dpg
from theme_settings import *
import webbrowser

welcome_window_id = dpg.generate_uuid()
welcome_window_image_size_id = dpg.generate_uuid()


def run_welcome_window(screen_width: int, screen_height: int):

    with dpg.window(label="Welcome to SimpleDrawing", no_resize=True, no_close=True, no_move=True,
                    width=250, height=290, pos=[int(screen_width / 2) - 125, int(screen_height / 2) - 145],
                    modal=True, show=True, no_collapse=True, id=welcome_window_id) as welcome_window:

        dpg.set_item_theme(welcome_window, theme=welcome_window_theme)

        dpg.add_dummy(height=5)
        dpg.add_separator()
        dpg.add_dummy(height=5)
        new_project_button = dpg.add_button(label='Create a new drawing', width=-1, callback=close_welcome_window)
        dpg.add_dummy(height=5)
        open_project_button = dpg.add_button(label='Open a drawing', width=-1)
        dpg.add_dummy(height=5)
        open_image_button = dpg.add_button(label='Open an image to edit', width=-1)
        dpg.add_dummy(height=5)
        exit_button = dpg.add_button(label='Exit SimpleDrawing', width=-1, callback=dpg.stop_dearpygui)
        dpg.add_dummy(height=5)
        dpg.add_separator()
        dpg.add_dummy(height=5)
        about_button = dpg.add_button(label="Read the docs", width=-1, callback=open_docs)

        dpg.set_item_font(welcome_window, bold_font)
        dpg.set_item_font(new_project_button, regular_font)
        dpg.set_item_font(open_project_button, regular_font)
        dpg.set_item_font(exit_button, regular_font)
        dpg.set_item_font(about_button, regular_font)
        dpg.set_item_font(open_image_button, regular_font)

    # with dpg.window(no_resize=True, no_close=True, no_move=True, no_title_bar=True,
    #                 autosize=True, pos=[int(screen_width / 2 + 135), int(screen_height / 2) - 110],
    #                 modal=False, show=True, no_collapse=True, id=welcome_window_image_size_id) as welcome_window_image_size:
    #
    #     dpg.set_item_theme(welcome_window_image_size, theme=welcome_window_theme)
    #     dpg.add_input_int(label="Width", step=0, width=100, min_value=1, default_value=1920)
    #     dpg.add_dummy(height=5)
    #     dpg.add_input_int(label="Height", step=0, width=100, min_value=1, default_value=1080)
    #     dpg.add_dummy(height=5)
    #     with dpg.group(horizontal=True):
    #         dpg.add_button(label="OK", width=80)
    #         dpg.add_button(label="Cancel", width=80)


def open_docs():
    webbrowser.open('https://github.com/RahulShagri/SimpleDrawing-Desktop-App#readme')


def close_welcome_window():
    dpg.delete_item(item=welcome_window_id)
