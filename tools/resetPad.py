from dearpygui.core import *

def resetPad(pad_name):
    # Erase all lines from the drawing pad
    clear_drawing(pad_name)
    set_item_color(pad_name, style=mvGuiCol_WindowBg, color=[255, 255, 255])