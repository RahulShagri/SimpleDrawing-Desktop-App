from dearpygui.core import *
from db_manage import reset_db

def resetPad(pad_name):
    # Erase all lines from the drawing pad
    clear_drawing(pad_name)
    set_item_color("Drawing Pad", style=mvGuiCol_WindowBg, color=[255, 255, 255])
    reset_db()
