import dearpygui.dearpygui as dpg

from windows.screen_resolution import get_screen_resolution
from theme_settings import *

# Record screen resolution
screen_width, screen_height = get_screen_resolution()

# Subtract Taskbar and title bar height
screen_height = screen_height - int(0.05*screen_height)

# Set up the base layout for all child windows
with dpg.window(label="Base window", no_title_bar=True, width=screen_width,
                height=screen_height, pos=[0, 0], no_resize=True, no_close=True, no_move=True) as base_window:

    with dpg.menu_bar(label="Menu Bar") as menu_bar_top:
        dpg.set_item_theme(item=menu_bar_top, theme=menu_bar_theme)

    with dpg.child(label="Tool Bar", autosize_x=True, height=50, horizontal_scrollbar=True, no_scrollbar=True) as tool_bar:
        dpg.set_item_theme(item=tool_bar, theme=tool_bar_theme)

        with dpg.group(horizontal=True, parent=tool_bar) as tool_group:
            dpg.add_dummy()

    with dpg.group(horizontal=True):
        with dpg.child(label="Drawing Pad", height=int(0.82*screen_height), width=int(0.83*screen_width)) as drawing_window:
            dpg.set_item_theme(item=drawing_window, theme=drawing_pad_theme)

            with dpg.plot(height=int(0.82*screen_height), width=int(0.83*screen_width), no_title=True,
                          pan_button=dpg.mvMouseButton_Middle, equal_aspects=True, no_box_select=True, no_menus=True) as drawing_pad:
                dpg.draw_rectangle(pmin=[0,0], pmax=[1920, 1080], color=[255,255,255], fill=[255,255,255], thickness=0)

        with dpg.group():
            with dpg.child(label="Tool Properties", height=int(0.4*screen_height), autosize_x=True) as tool_properties:
                dpg.set_item_theme(item=tool_properties, theme=tool_properties_theme)

            with dpg.child(label="Layer Properties", height=int(0.42*screen_height) - 4, autosize_x=True) as layer_properties:
                dpg.set_item_theme(item=layer_properties, theme=layer_properties_theme)

    with dpg.child(label="Info Bar", height=20, autosize_x=True) as info_bar:
        dpg.set_item_theme(item=info_bar, theme=info_bar_theme)
        dpg.set_item_font(item=info_bar, font=small_font)
