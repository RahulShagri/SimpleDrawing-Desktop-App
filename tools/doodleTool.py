from dearpygui.core import *
import time

line_count = 0

def doodleTool(pad_name, lineColor, lineThickness):
    print("\nDoodle tool initiated.")

    global line_count

    time.sleep(0.1)

    while True:
        if is_mouse_button_released(mvMouseButton_Left):

            # -----If mouse is clicked outside the Drawing Pad, exit the tool.-----#
            if get_active_window() != "Drawing Pad":
                print("\nDoodle line tool terminated.")
                return

            # -----Continue of clicked on the pad_name-----#
            mouse_position = get_drawing_mouse_pos()
            time.sleep(0.01)

            doodleCoordinates = [mouse_position]

            while True:
                # -----Draw line-----#
                doodleCoordinates.append(get_drawing_mouse_pos())
                draw_polyline(pad_name, points=doodleCoordinates, color=lineColor, thickness=lineThickness, tag=f"doodle {line_count}")

                time.sleep(0.01)

                # -----Check if user wants to exit the line tool-----#
                if is_mouse_button_released(mvMouseButton_Left):
                    line_count += 1
                    time.sleep(0.01)
                    print("\nDoodle line tool terminated.")
                    return

                # -----Check if user wants to exit the line tool-----#
                if is_mouse_button_released(mvMouseButton_Right):
                    delete_draw_command(pad_name, f"doodle {line_count}")
                    print("\nDoodle line tool terminated.")
                    return

                # -----Check if user wants to exit the line tool-----#
                if is_key_released(mvKey_Escape):
                    delete_draw_command(pad_name, f"doodle {line_count}")
                    print("\nDoodle line tool terminated.")
                    return

                # -----Delete the line drawn and begin the process again till user clicks the second point or exits the tool-----#
                line_count += 1
                delete_draw_command(pad_name, f"doodle {line_count}")