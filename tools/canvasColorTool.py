from dearpygui.core import *

def canvasColorTool(pad_name, canvasColor):
    delete_draw_command(pad_name, "canvas background")
    draw_rectangle(pad_name, pmin=[0, 0], pmax=[1025, 629], color=canvasColor, fill=canvasColor, thickness=2,
                   tag="canvas background")