from dearpygui.core import *
from dearpygui.simple import *
import tools

def hotkeyCommands():
    if is_key_down(mvKey_Control):
        if is_key_released(mvKey_S):
            tools.saveImageTool()