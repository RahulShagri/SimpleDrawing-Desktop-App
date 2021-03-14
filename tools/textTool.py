from dearpygui.core import *
import time

textCount = 0

def textTool(pad_name, userText, textColor, textSize):
    print("\nText tool initiated.")

    global textCount    #Keeping a track of the number of straight lines

    time.sleep(0.1)

    while True:
        # Begin drawing when left mouse button is released
        if is_mouse_button_released(mvMouseButton_Left):
            # If mouse is clicked outside the Drawing Pad, exit the tool.
            if get_active_window() != "Drawing Pad":
                print("\nText tool terminated.")
                return

            time.sleep(0.01)

            while True:
                # Draw text
                draw_text(pad_name, pos=get_drawing_mouse_pos(), text=userText, color=textColor, size=textSize, tag=f"text {textCount}")
                time.sleep(0.01)

                # Check if user wants to select the second point of the line
                if is_mouse_button_released(mvMouseButton_Left):
                    # If the user clicks outside the drawing pad, it is assumed that they want to terminate the tool
                    if get_active_window() != "Drawing Pad":
                        delete_draw_command(pad_name, f"text {textCount}")
                        print("\nText tool terminated.")
                        return

                    textCount += 1
                    time.sleep(0.01)
                    return

                # Check if user wants to exit the line tool
                if is_mouse_button_released(mvMouseButton_Right):
                    delete_draw_command(pad_name, f"text {textCount}")
                    print("\nText tool terminated.")
                    return

                # Check if user wants to exit the line tool
                if is_key_released(mvKey_Escape):
                    delete_draw_command(pad_name, f"text {textCount}")
                    print("\nText tool terminated.")
                    return

                # Delete the line drawn and begin the process again till user clicks the second point or exits the tool
                delete_draw_command(pad_name, f"text {textCount}")