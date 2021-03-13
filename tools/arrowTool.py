from dearpygui.core import *
import time

arrowCount = 0

def arrowTool(pad_name, arrowColor, lineThickness, arrowSize):
    print("\nArrow tool initiated.")

    global arrowCount    #Keeping a track of the number of arrows

    time.sleep(0.1)

    while True:
        # Begin drawing when left mouse button is released
        if is_mouse_button_released(mvMouseButton_Left):

            # If mouse is clicked outside the Drawing Pad, exit the tool.
            if get_active_window() != "Drawing Pad":
                print("\nArrow tool terminated.")
                return

            # Continue of clicked on the drawing pad
            mouse_position = get_drawing_mouse_pos()
            time.sleep(0.01)

            while True:
                # Draw line
                draw_arrow(pad_name, p1=mouse_position, p2=get_drawing_mouse_pos(), color=arrowColor, thickness=lineThickness, size=arrowSize, tag=f"arrow {arrowCount}")
                time.sleep(0.01)

                # Check if user wants to select the second point of the line
                if is_mouse_button_released(mvMouseButton_Left):
                    # If the user clicks outside the drawing pad, it is assumed that they want to terminate the tool
                    if get_active_window() != "Drawing Pad":
                        delete_draw_command(pad_name, f"arrow {arrowCount}")
                        print("\nArrow line tool terminated.")
                        return

                    arrowCount += 1
                    time.sleep(0.01)
                    return

                # Check if user wants to exit the line tool
                if is_mouse_button_released(mvMouseButton_Right):
                    delete_draw_command(pad_name, f"arrow {arrowCount}")
                    return

                # Check if user wants to exit the line tool
                if is_key_released(mvKey_Escape):
                    delete_draw_command(pad_name, f"arrow {arrowCount}")
                    return

                # Delete the line drawn and begin the process again till user clicks the second point or exits the tool
                delete_draw_command(pad_name, f"arrow {arrowCount}")