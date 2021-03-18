import win32gui
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os

from db_manage import open_db

from dearpygui.core import *

file_path = ''


def openTool():
    global file_path

    delete_draw_command("Pad", "cursorX")
    delete_draw_command("Pad", "cursorY")

    Tk().withdraw()

    hwnd = win32gui.FindWindow(None, "SimpleDrawing")

    file_path = askopenfilename(title="SimpleDrawing open drawing window",
                                filetypes=[("SimpleDrawing File (*.db)", "*.db")],
                                defaultextension=[("SimpleDrawing File (*.db)", "*.db")])

    win32gui.SetForegroundWindow(hwnd)

    if file_path:
        open_db(file_path)