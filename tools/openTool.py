import pyautogui
import win32gui, win32con
import time
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
    win32gui.SetForegroundWindow(hwnd)

    file_path = askopenfilename(title="SimpleDrawing save image window",
                                initialfile="New SimpleDrawing",
                                filetypes=[("SimpleDrawing File (*.db)", "*.db")],
                                defaultextension=[("SimpleDrawing File (*.db)", "*.db")])

    win32gui.SetForegroundWindow(hwnd)

    if file_path:
        open_db(file_path)