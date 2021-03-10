from dearpygui.core import *
import time

straightLineCount = 0

def straightLineTool(pad_name, lineColor, lineThickness):
    print("\nStraight line tool initiated.")

    global straightLineCount    #Keeping a track of the nubmer of straight lines

    time.sleep(0.1)

    while True:
        #-----Begin drawing when left mouse button is released-----#
        if is_mouse_button_released(mvMouseButton_Left):

            #-----If mouse is clicked outide the Drowing Pad, exit the tool.-----#
            if get_active_window() != "Drawing Pad":
                print("\nStraight line tool terminated.")
                return

            #-----Continue of clicked on the drawing pad-----#
            mouse_position = get_drawing_mouse_pos()
            time.sleep(0.01)

            while True:
                #-----Draw line-----#
                draw_line(pad_name, p1=mouse_position, p2=get_drawing_mouse_pos(), color=lineColor, thickness=lineThickness, tag=f"straightLine {straightLineCount}")
                time.sleep(0.01)
                line_flag = 1

                #-----Check if user wants to select the second point of the line-----#
                if is_mouse_button_released(mvMouseButton_Left):
                    #-----If the user clicks outside the drawing pad, it is assumed that they want to terminate the tool-----#
                    if get_active_window() != "Drawing Pad":
                        delete_draw_command(pad_name, f"straightLine {straightLineCount}")
                        print("\nStraight line tool terminated.")
                        return

                    straightLineCount += 1
                    time.sleep(0.01)
                    return

                #-----Check if user wants to exit the line tool-----#
                if is_mouse_button_released(mvMouseButton_Right):
                    delete_draw_command(pad_name, f"straightLine {straightLineCount}")
                    return

                #-----Check if user wants to exit the line tool-----#
                if is_key_released(mvKey_Escape):
                    delete_draw_command(pad_name, f"straightLine {straightLineCount}")
                    return

                #-----Delete the line drawn and begin the process again till user clicks the second point or exits the tool-----#
                delete_draw_command(pad_name, f"straightLine {straightLineCount}")