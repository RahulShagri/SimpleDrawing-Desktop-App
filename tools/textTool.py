from dearpygui.core import *
import time

from db_manage import *


def textTool(pad_name, userText, textColor, textSize):

    time.sleep(0.1)

    while True:
        # Begin drawing when left mouse button is released
        if is_mouse_button_released(mvMouseButton_Left):
            # If mouse is clicked outside the Drawing Pad, exit the tool.
            if get_active_window() != "Drawing Pad":
                break

            time.sleep(0.01)

            while True:
                # Draw text
                point = get_drawing_mouse_pos()
                draw_text(pad_name, pos=point, text=userText, color=textColor, size=textSize, tag=f"text {tools.text_count}")
                time.sleep(0.01)

                # Check if user wants to select the second point of the line
                if is_mouse_button_released(mvMouseButton_Left):
                    # If the user clicks outside the drawing pad, it is assumed that they want to terminate the tool
                    if get_active_window() != "Drawing Pad":
                        delete_draw_command(pad_name, f"text {tools.text_count}")
                        break

                    write_db(tool="text tool", point_1=str(point), text=userText, color=str(textColor), size=textSize,
                             tag=f"text {tools.text_count}")

                    tools.text_count += 1
                    time.sleep(0.01)
                    break

                # Check if user wants to exit the line tool
                if is_mouse_button_released(mvMouseButton_Right):
                    delete_draw_command(pad_name, f"text {tools.text_count}")
                    break

                # Check if user wants to exit the line tool
                if is_key_released(mvKey_Escape):
                    delete_draw_command(pad_name, f"text {tools.text_count}")
                    break

                # Delete the line drawn and begin the process again till user clicks the second point or exits the tool
                delete_draw_command(pad_name, f"text {tools.text_count}")