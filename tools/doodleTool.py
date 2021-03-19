from dearpygui.core import *
import time
from db_manage import *

def doodleTool(pad_name, lineColor, lineThickness):

    time.sleep(0.1)

    while True:
        if is_mouse_button_released(mvMouseButton_Left):

            # If mouse is clicked outside the Drawing Pad, exit the tool.
            if get_active_window() != "Drawing Pad":
                break

            # Continue of clicked on the pad_name
            mouse_position = get_drawing_mouse_pos()
            time.sleep(0.01)

            doodleCoordinates = [mouse_position]

            while True:
                # Draw line
                doodleCoordinates.append(get_drawing_mouse_pos())
                draw_polyline(pad_name, points=doodleCoordinates, color=lineColor, thickness=lineThickness, tag=f"doodle {tools.doodle_count}")

                time.sleep(0.01)

                # Check if user wants to exit the line tool
                if is_mouse_button_released(mvMouseButton_Left):
                    write_db(tool="doodle tool", point_1=str(doodleCoordinates), color=str(lineColor), thickness=lineThickness, tag=f"doodle {tools.doodle_count}")
                    tools.doodle_count += 1
                    time.sleep(0.01)
                    break

                # Check if user wants to exit the line tool
                if is_mouse_button_released(mvMouseButton_Right):
                    delete_draw_command(pad_name, f"doodle {tools.doodle_count}")
                    break

                # Check if user wants to exit the line tool
                if is_key_released(mvKey_Escape):
                    delete_draw_command(pad_name, f"doodle {tools.doodle_count}")
                    break

                delete_draw_command(pad_name, f"doodle {tools.doodle_count}")
