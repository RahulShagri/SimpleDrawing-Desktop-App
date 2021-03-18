from dearpygui.core import *

from db_manage import *

current_canvas_color = [255, 255, 255, 255]

def canvasColorTool(pad_name, canvasColor):
    global current_canvas_color
    set_item_color(pad_name, style=mvGuiCol_WindowBg, color=canvasColor)
    write_db(tool="canvas color tool", canvasBefore=str(current_canvas_color), canvasAfter=str(canvasColor))
    current_canvas_color = canvasColor
