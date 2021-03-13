from dearpygui.core import *

def resetPad(pad_name):
    # Erase all lines from the drawing pad
    clear_drawing(pad_name)
    draw_rectangle("Pad", pmin=[0, 0], pmax=[1025, 629], color=[255, 255, 255], fill=[255, 255, 255], thickness=2,
                   tag="canvas background")