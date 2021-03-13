from dearpygui.core import *
import time

bezier_count = 0

def bezierTool(pad_name, lineColor, lineThickness):
    print("\nBezier tool initiated.")

    global bezier_count
    temp_polyline_count = 0

    bezier_points = []

    time.sleep(0.1)
    while True:
        if is_mouse_button_released(mvMouseButton_Left):

            # If mouse is clicked outside the Drawing Pad, exit the tool.
            if get_active_window() != "Drawing Pad":
                print("\nBezier tool terminated.")
                return

            # Continue of clicked on the drawing pad
            bezier_points.append(get_drawing_mouse_pos())
            mouse_position = get_drawing_mouse_pos()
            time.sleep(0.01)

            while True:
                # Draw line
                point2 = get_drawing_mouse_pos()
                draw_line(pad_name, p1=mouse_position, p2=point2, color=lineColor, thickness=1, tag=f"polyLine {temp_polyline_count}")

                time.sleep(0.01)

                # Check if user wants to select more points for the polyline
                if is_mouse_button_released(mvMouseButton_Left):
                    # If the user clicks outside the drawing pad, it is assumed that they want to terminate the tool
                    if get_active_window() != "Drawing Pad":
                        for count in range(temp_polyline_count+1):
                            delete_draw_command(pad_name, f"polyLine {count}")

                        print("\nBezier tool terminated.")
                        return

                    temp_polyline_count += 1
                    mouse_position = point2
                    bezier_points.append(point2)

                    if temp_polyline_count == 2:
                        while True:
                            point4 = get_drawing_mouse_pos()

                            draw_line(pad_name, p1=bezier_points[2], p2=get_drawing_mouse_pos(), color=lineColor, thickness=1, tag=f"polyline {temp_polyline_count}")
                            draw_bezier_curve(pad_name, p1=bezier_points[0], p2=bezier_points[1], p3=bezier_points[2],
                                              p4=point4, color=lineColor, thickness=lineThickness,
                                              tag=f"bezier {bezier_count}")

                            time.sleep(0.02)

                            if is_mouse_button_released(mvMouseButton_Left):
                                # Deleting reference poly-lines
                                delete_draw_command(pad_name, f"polyline {temp_polyline_count}")
                                for count in range(temp_polyline_count):
                                    delete_draw_command(pad_name, f"polyLine {count}")

                                if get_active_window() != "Drawing Pad":
                                    delete_draw_command(pad_name, f"bezier {bezier_count}")
                                    print("\nBezier tool terminated.")
                                    return

                                bezier_count += 1
                                time.sleep(0.01)
                                return

                            # Check if user wants to exit the line tool
                            if is_mouse_button_released(mvMouseButton_Right):
                                # Deleting reference poly-lines
                                delete_draw_command(pad_name, f"polyline {temp_polyline_count}")
                                for count in range(temp_polyline_count):
                                    delete_draw_command(pad_name, f"polyLine {count}")

                                delete_draw_command(pad_name, f"bezier {bezier_count}")
                                return

                            # Check if user wants to exit the line tool
                            if is_key_released(mvKey_Escape):
                                # Deleting reference poly-lines
                                delete_draw_command(pad_name, f"polyline {temp_polyline_count}")
                                for count in range(temp_polyline_count):
                                    delete_draw_command(pad_name, f"polyLine {count}")

                                delete_draw_command(pad_name, f"bezier {bezier_count}")
                                return

                            # Delete the line drawn and begin the process again till user clicks the second point or exits the tool
                            delete_draw_command(pad_name, f"polyline {temp_polyline_count}")
                            delete_draw_command(pad_name, f"bezier {bezier_count}")

                    time.sleep(0.01)

                # Check if user wants to exit the tool
                if is_mouse_button_released(mvMouseButton_Right):
                    # Deleting reference poly-lines
                    for count in range(temp_polyline_count):
                        delete_draw_command(pad_name, f"polyLine {count}")

                    print("\nBezier tool terminated.")
                    return

                # Check if user wants to exit the line tool
                if is_key_released(mvKey_Escape):
                    # Deleting reference poly-lines
                    for count in range(temp_polyline_count):
                        delete_draw_command(pad_name, f"polyLine {count}")

                    print("\nBezier tool terminated.")
                    return

                # Delete the line drawn and begin the process again till user clicks the second point or exits the tool
                delete_draw_command(pad_name, f"polyLine {temp_polyline_count}")