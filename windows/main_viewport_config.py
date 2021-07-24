# Configuring the main viewport
import dearpygui.dearpygui as dpg
from windows.screen_resolution import get_screen_resolution

screen_width, screen_height = get_screen_resolution()

dpg.setup_viewport()
dpg.set_viewport_title("SimpleDrawing")
dpg.configure_viewport(0, x_pos=0, y_pos=0, width=screen_width, height=(screen_height - int(0.05*screen_height)))
