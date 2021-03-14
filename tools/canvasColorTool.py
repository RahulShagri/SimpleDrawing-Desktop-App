from dearpygui.core import *


def canvasColorTool(pad_name, canvasColor):
    set_item_color(pad_name, style=mvGuiCol_WindowBg, color=canvasColor)