from dearpygui.core import *
import tools
import time

from db_manage import *

def hotkeyCommands():
    if is_key_down(mvKey_Control):
        if is_key_pressed(mvKey_S):
            tools.saveTool()
            return

        elif is_key_pressed(mvKey_O):
            tools.openTool()
            return

        elif is_key_pressed(mvKey_Z):
            read_db(action='undo')
            time.sleep(0.2)
            return

        elif is_key_pressed(mvKey_Y):
            read_db(action='redo')
            time.sleep(0.2)
            return

