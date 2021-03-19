from dearpygui.core import *
import time
import math
from db_manage import *
from PIL import Image

import pyautogui
import win32gui, win32con
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def imageTool(pad_name, file):
    image = Image.open(file)
    width, height = image.size
    aspect_ratio = width/height
    time.sleep(0.1)

    while True:
        # Begin drawing when left mouse button is released
        if is_mouse_button_released(mvMouseButton_Left):

            # If mouse is clicked outside the Drawing Pad, exit the tool.
            if get_active_window() != "Drawing Pad":
                break

            # Continue if clicked on the drawing pad
            mouse_position = get_drawing_mouse_pos()
            time.sleep(0.01)

            while True:
                point2 = get_drawing_mouse_pos()

                if is_key_down(mvKey_Shift):
                    if point2[0] < mouse_position[0]:
                        # Check if in second quadrant
                        if point2[1] < mouse_position[1]:
                            first_point = mouse_position
                            width = aspect_ratio * (mouse_position[1] - point2[1])
                            second_point = [mouse_position[0] - width, point2[1]]
                            draw_image(pad_name, pmin=first_point, pmax=second_point, file=file, tag=f"image {tools.image_count}")

                        # Check if in third quadrant
                        else:
                            first_point = mouse_position
                            width = aspect_ratio * (point2[1] - mouse_position[1])
                            second_point = [mouse_position[0] - width, point2[1]]
                            draw_image(pad_name, pmin=first_point, pmax=second_point, file=file, tag=f"image {tools.image_count}")

                    # Check if in first quadrant
                    elif get_drawing_mouse_pos()[1] < mouse_position[1]:
                        first_point = mouse_position
                        width = aspect_ratio * (mouse_position[1] - point2[1])
                        second_point = [mouse_position[0] + width, point2[1]]
                        draw_image(pad_name, pmin=first_point, pmax=second_point, file=file, tag=f"image {tools.image_count}")

                    # Check if in fourth quadrant
                    else:
                        first_point = mouse_position
                        width = aspect_ratio * (point2[1] - mouse_position[1])
                        second_point = [mouse_position[0] + width, point2[1]]
                        draw_image(pad_name, pmin=first_point, pmax=second_point, file=file, tag=f"image {tools.image_count}")

                else:
                    first_point = mouse_position
                    second_point = point2
                    draw_image(pad_name, pmin=first_point, pmax=second_point, file=file, tag=f"image {tools.image_count}")

                time.sleep(0.01)

                # Check if user wants to select the second point of the line
                if is_mouse_button_released(mvMouseButton_Left):
                    # If the user clicks outside the drawing pad, it is assumed that they want to terminate the tool
                    if get_active_window() != "Drawing Pad":
                        delete_draw_command(pad_name, f"image {tools.image_count}")
                        break

                    write_db(tool="image tool", point_1=str(first_point), point_2=str(second_point), image=file, tag=f"image {tools.image_count}")
                    tools.image_count += 1
                    time.sleep(0.01)
                    break

                # Check if user wants to exit the line tool
                if is_mouse_button_released(mvMouseButton_Right):
                    delete_draw_command(pad_name, f"image {tools.image_count}")
                    break

                # Check if user wants to exit the line tool
                if is_key_released(mvKey_Escape):
                    delete_draw_command(pad_name, f"image {tools.image_count}")
                    break

                # Delete the line drawn and begin the process again till user clicks the second point or exits the tool
                delete_draw_command(pad_name, f"image {tools.image_count}")

def get_angle(first_position, second_position):

    if second_position[0] == first_position[0]:
        return 0

    else:
        return abs(math.degrees(math.atan((second_position[1] - first_position[1]) / (second_position[0] - first_position[0]))))

def searchImage():
    Tk().withdraw()

    hwnd = win32gui.FindWindow(None, "SimpleDrawing")

    file_path = askopenfilename(title="SimpleDrawing select image window",
                                filetypes=[("JPEG (*.jpg, *.jpeg)", "*.jpg"), ("PNG (*.png)", "*.png")],
                                defaultextension=[("JPEG (*.jpg, *.jpeg)", "*.jpg"), ("PNG (*.png)", "*.png")])

    win32gui.SetForegroundWindow(hwnd)

    if file_path:
        set_value("##imagePath", file_path)