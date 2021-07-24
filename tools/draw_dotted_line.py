import dearpygui.dearpygui as dpg
import math


line_ids = []
temp_count = 0


def draw_dotted_line(p1: list[float], p2: list[float], color: list[float], spacing: float, radius: float, parent: int):
    global line_ids, temp_count

    line_ids.append(dpg.generate_uuid())

    # Handling Horizontal lines
    if p1[1] == p2[1]:

        # When mouse is to the left of the first point
        if p2[0] < p1[0]:
            temp = p1
            p1 = p2
            p2 = temp
            del temp

        first_centre = p1[:]
        second_centre = p1[:]

        while True:
            second_centre[0] += spacing

            if second_centre[0] <= p2[0]:
                dpg.draw_circle(center=first_centre, radius=radius, color=color, fill=color, parent=parent,
                              id=line_ids[temp_count])
                line_ids.append(dpg.generate_uuid())
                temp_count += 1

            else:
                break

            second_centre[0] += spacing

            if second_centre[0] < p2[0]:
                first_centre = second_centre[:]
            else:
                break

    # Handling all lines except horizontal lines
    else:

        if p2[1] < p1[1]:
            temp = p1
            p1 = p2
            p2 = temp
            del temp

        length = pow((pow((p2[0] - p1[0]), 2) + pow((p2[1] - p1[1]), 2)), 0.5)

        first_centre = p1

        if p2[0] >= p1[0]:
            angle = math.atan((p2[0] - p1[0]) / (p2[1] - p1[1]))

            while True:
                x_co = first_centre[0] + spacing * math.sin(angle)
                y_co = first_centre[1] + spacing * math.cos(angle)

                second_centre = [x_co, y_co]

                if second_centre[0] <= p2[0] and second_centre[1] <= p2[1]:

                    dpg.draw_circle(center=first_centre, radius=radius, color=color, fill=color, parent=parent,
                                  id=line_ids[temp_count])
                    line_ids.append(dpg.generate_uuid())
                    temp_count += 1
                    length -= spacing

                else:
                    second_centre[0] -= spacing * math.sin(angle)
                    second_centre[1] -= spacing * math.cos(angle)
                    dpg.draw_circle(center=second_centre, radius=radius, color=color, fill=color, parent=parent,
                                  id=line_ids[temp_count])
                    line_ids.append(dpg.generate_uuid())
                    temp_count += 1
                    break

                if length >= spacing:
                    first_centre = second_centre
                    x_co = first_centre[0] + spacing * math.sin(angle)
                    y_co = first_centre[1] + spacing * math.cos(angle)
                    second_centre = [x_co, y_co]
                    first_centre = second_centre
                    length -= spacing

                else:
                    break

        elif p2[0] < p1[0]:
            angle = math.atan((p1[0] - p2[0]) / (p2[1] - p1[1]))

            while True:
                x_co = first_centre[0] - spacing * math.sin(angle)
                y_co = first_centre[1] + spacing * math.cos(angle)

                second_centre = [x_co, y_co]

                if second_centre[0] >= p2[0] and second_centre[1] <= p2[1]:

                    dpg.draw_circle(center=first_centre, radius=radius, color=color, fill=color, parent=parent,
                                  id=line_ids[temp_count])
                    line_ids.append(dpg.generate_uuid())
                    temp_count += 1
                    length -= spacing

                else:
                    second_centre[0] += spacing * math.sin(angle)
                    second_centre[1] -= spacing * math.cos(angle)
                    dpg.draw_circle(center=second_centre, radius=radius, color=color, fill=color, parent=parent,
                                  id=line_ids[temp_count])
                    line_ids.append(dpg.generate_uuid())
                    temp_count += 1
                    break

                if length >= spacing:
                    first_centre = second_centre
                    x_co = first_centre[0] - spacing * math.sin(angle)
                    y_co = first_centre[1] + spacing * math.cos(angle)
                    second_centre = [x_co, y_co]
                    first_centre = second_centre
                    length -= spacing

                else:
                    break


def clear_dotted_line(new_line_flag = 0):
    global line_ids, temp_count
    if new_line_flag == 1:
        line_ids = []
        temp_count = 0
        return

    for id in line_ids:
        if dpg.does_item_exist(item=id):
            dpg.delete_item(item=id)


