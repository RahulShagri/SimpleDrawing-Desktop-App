import pyautogui
import win32gui, win32con
import time
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename
from PIL import Image
import os

from dearpygui.core import *

file_path = ''

def saveImageTool():
    global file_path

    delete_draw_command("Pad", "cursorX")
    delete_draw_command("Pad", "cursorY")

    Tk().withdraw()

    hwnd = win32gui.FindWindow(None, "SimpleDrawing")
    win32gui.SetForegroundWindow(hwnd)
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    time.sleep(0.1)
    x, y, x1, y1 = win32gui.GetClientRect(hwnd)
    x, y = win32gui.ClientToScreen(hwnd, (x, y))
    x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
    im = pyautogui.screenshot(region=(x, y, x1, y1))
    im = pyautogui.screenshot()
    file_path = asksaveasfilename(title="SimpleDrawing save image window",
                                  initialfile="New SimpleDrawing",
                                  filetypes=[("JPEG (*.jpg, *.jpeg)", "*.jpg"), ("PNG (*.png)", "*.png"), ("PDF (*.pdf)", "*.pdf")],
                                  defaultextension= [("JPEG (*.jpg, *.jpeg)", "*.jpg"), ("PNG (*.png)", "*.png"), ("PDF (*.pdf)", "*.pdf")])
    if file_path:

        if file_path[-4:] == ".pdf":
            im.save(f"{file_path[:-4]}.png")
            im = Image.open(f"{file_path[:-4]}.png")
            im = im.crop((335, 80, 1352, 683))
            im.save(f"{file_path[:-4]}.png")
            im = im.convert('RGB')
            im.save(fr'{file_path}')
            os.remove(f"{file_path[:-4]}.png")

        else:
            im.save(file_path)
            im = Image.open(file_path)
            im = im.crop((335, 80, 1352, 683))
            im.save(file_path)

'''def savePDFTool():
    global file_path

    saveImageTool()
    image = Image.open(fr'{file_path}')
    image = image.convert('RGB')
    image.save(fr"{file_path[:-4]}.pdf")'''