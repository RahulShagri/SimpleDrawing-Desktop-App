from dearpygui.core import *
from dearpygui.simple import *
import time

line_count = 0

def line_tool():
    global line_count

    if is_key_down(mvKey_Control):
        if is_key_released(mvKey_Z):
            if line_count > 0:
                delete_series("new plot", f"line {line_count}")
                line_count -= 1
            print(line_count)

    if is_mouse_button_released(mvMouseButton_Left):
        set_value("Left mouse released", "True")
        mouse_position = get_plot_mouse_pos()
        line_count += 1
        print(f'line number {line_count}')

        time.sleep(0.02)

        while True:
            if is_mouse_button_released(mvMouseButton_Left):
                set_value("Left mouse released", "True")
                time.sleep(0.02)
                return
            else:
                set_value("Left mouse released", "False")
                add_line_series("new plot", f"line {line_count}", x=[mouse_position[0], get_plot_mouse_pos()[0]],
                                y=[mouse_position[1], get_plot_mouse_pos()[1]])

                if is_key_released(mvKey_Escape):
                    set_value("Escape button released", "True")
                    delete_series("new plot", f"line {line_count}")
                    return

                else:
                    set_value("Escape button released", "False")
    else:
        set_value("Left mouse released", "False")
        return


with window("Main Window"):
    add_label_text("Mouse position", default_value="(0, 0)", color=[0, 200, 255])
    add_label_text("Left mouse released", default_value="False", color=[0, 200, 255])
    add_label_text("Escape button released", default_value="False", color=[0, 200, 255])
    add_label_text("Control button down", default_value="False", color=[0, 200, 255])
    add_label_text("Z button released", default_value="False", color=[0, 200, 255])

    add_plot("new plot", yaxis_lock_min=True, xaxis_lock_min=True, yaxis_lock_max=True, xaxis_lock_max=True, no_legend=True, no_menus=True, no_box_select=True, no_mouse_pos=True, xaxis_no_gridlines=True, yaxis_no_gridlines=True, label='Drawing Pad', xaxis_no_tick_marks=True, xaxis_no_tick_labels=True, yaxis_no_tick_labels=True, yaxis_no_tick_marks=True)
    add_line_series("new plot", "bounding box", x=[0, 1, 1, 0], y=[0, 0, 1, 1])

def main_callback(sender, data):
    set_value("Mouse position", get_plot_mouse_pos())

    if is_key_released(mvKey_Escape):
        set_value("Escape button released", "True")
        return

    else:
        set_value("Escape button released", "False")

    if is_key_down(mvKey_Control):
        set_value("Control button down", "True")
        if is_key_released(mvKey_Z):
            set_value("Z button released", "True")
            return

        else:
            set_value("Z button released", "False")
        return

    else:
        set_value("Control button down", "False")

    if is_key_released(mvKey_Z):
        set_value("Z button released", "True")
        return

    else:
        set_value("Z button released", "False")

set_render_callback(main_callback)
set_mouse_release_callback(line_tool)
set_key_down_callback(line_tool)

start_dearpygui(primary_window="Main Window")