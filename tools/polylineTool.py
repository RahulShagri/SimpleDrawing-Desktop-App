from dearpygui.core import *
import time

polyLine_count = 0

def polylineTool(pad_name, lineColor, lineThickness):
    print("\nPolyline tool initiated.")

    global polyLine_count

    time.sleep(0.1)
    while True:
        if is_mouse_button_released(mvMouseButton_Left):

            #-----If mouse is clicked outide the Drowing Pad, exit the tool.-----#
            if get_active_window() != "Drawing Pad":
                print("\nPolyline tool terminated.")
                return

            #-----Continue of clicked on the drawing pad-----#
            mouse_position = get_drawing_mouse_pos()
            time.sleep(0.01)

            while True:
                #-----Draw line-----#
                point2 = get_drawing_mouse_pos()
                draw_line(pad_name, p1=mouse_position, p2=point2, color=lineColor, thickness=lineThickness, tag=f"polyLine {polyLine_count}")

                time.sleep(0.01)
                line_flag = 1

                #-----Check if user wants to select more points for the polyline-----#
                if is_mouse_button_released(mvMouseButton_Left):
                    # -----If the user clicks outside the drawing pad, it is assumed that they want to terminate the tool-----#
                    if get_active_window() != "Drawing Pad":
                        delete_draw_command(pad_name, f"polyLine {polyLine_count}")
                        print("\nPolyline tool terminated.")
                        return

                    polyLine_count += 1
                    mouse_position = point2
                    time.sleep(0.01)

                #-----Check if user wants to exit the line tool-----#
                if is_mouse_button_released(mvMouseButton_Right):
                    delete_draw_command(pad_name, f"polyLine {polyLine_count}")
                    print("\nPolyline tool terminated.")
                    return

                #-----Check if user wants to exit the line tool-----#
                if is_key_released(mvKey_Escape):
                    delete_draw_command(pad_name, f"polyLine {polyLine_count}")
                    print("\nPolyline tool terminated.")
                    return

                #-----Delete the line drawn and begin the process again till user clicks the second point or exits the tool-----#
                delete_draw_command(pad_name, f"polyLine {polyLine_count}")