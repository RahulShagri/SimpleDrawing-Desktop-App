import dearpygui.dearpygui as dpg
import math


line_ids = []
temp_count = 0


def draw_dot_dashed_line(p1: list[float], p2: list[float], color: list[float], thickness: float, spacing: float, radius: float, parent: int):
    global line_ids, temp_count

    line_ids.append(dpg.generate_uuid())

    # Handling Horizontal lines
    if p1[1] == p2[1]:

        if p2[0] < p1[0]:
            temp = p1
            p1 = p2
            p2 = temp
            del temp

        first_point = p1[:]
        second_point = p1[:]


        while True:
            second_point[0] += spacing

            if second_point[0] <= p2[0]:
                if temp_count % 2 == 0:
                    dpg.draw_line(p1=first_point, p2=second_point, color=color, thickness=thickness, parent=parent,
                                  id=line_ids[temp_count])

                else:
                    mid_point = [(first_point[0] + second_point[0])/2, (first_point[1] + second_point[1])/2]
                    dpg.draw_circle(center=mid_point, radius=radius, color=color, fill=color, parent=parent, id=line_ids[temp_count])

                line_ids.append(dpg.generate_uuid())
                temp_count += 1

            else:
                if temp_count % 2 == 0:
                    second_point[0] -= spacing
                    dpg.draw_line(p1=second_point, p2=p2, color=color, thickness=thickness, id=line_ids[temp_count],
                                  parent=parent)
                    line_ids.append(dpg.generate_uuid())
                    temp_count += 1
                break

            second_point[0] += spacing

            if second_point[0] < p2[0]:
                first_point = second_point[:]
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

        first_point = p1

        if p2[0] >= p1[0]:
            angle = math.atan((p2[0] - p1[0]) / (p2[1] - p1[1]))

            while True:
                x_co = first_point[0] + spacing * math.sin(angle)
                y_co = first_point[1] + spacing * math.cos(angle)

                second_point = [x_co, y_co]

                if second_point[0] <= p2[0] and second_point[1] <= p2[1]:
                    if temp_count % 2 == 0:
                        dpg.draw_line(p1=first_point, p2=second_point, color=color, thickness=thickness, parent=parent,
                                      id=line_ids[temp_count])
                    else:
                        mid_point = [(first_point[0] + second_point[0]) / 2, (first_point[1] + second_point[1]) / 2]
                        dpg.draw_circle(center=mid_point, radius=radius, color=color, fill=color, parent=parent,
                                        id=line_ids[temp_count])
                    line_ids.append(dpg.generate_uuid())
                    temp_count += 1
                    length -= spacing

                else:
                    if temp_count % 2 == 0:
                        second_point[0] -= spacing * math.sin(angle)
                        second_point[1] -= spacing * math.cos(angle)
                        dpg.draw_line(p1=second_point, p2=p2, color=color, thickness=thickness, parent=parent,
                                      id=line_ids[temp_count])
                        line_ids.append(dpg.generate_uuid())
                        temp_count += 1
                    break

                if length >= spacing:
                    first_point = second_point
                    x_co = first_point[0] + spacing * math.sin(angle)
                    y_co = first_point[1] + spacing * math.cos(angle)
                    second_point = [x_co, y_co]
                    first_point = second_point
                    length -= spacing

                else:
                    break

        elif p2[0] < p1[0]:
            angle = math.atan((p1[0] - p2[0]) / (p2[1] - p1[1]))

            while True:
                x_co = first_point[0] - spacing * math.sin(angle)
                y_co = first_point[1] + spacing * math.cos(angle)

                second_point = [x_co, y_co]

                if second_point[0] >= p2[0] and second_point[1] <= p2[1]:
                    if temp_count % 2 == 0:
                        dpg.draw_line(p1=first_point, p2=second_point, color=color, thickness=thickness, parent=parent,
                                      id=line_ids[temp_count])
                    else:
                        mid_point = [(first_point[0] + second_point[0]) / 2, (first_point[1] + second_point[1]) / 2]
                        dpg.draw_circle(center=mid_point, radius=radius, color=color, fill=color, parent=parent,
                                        id=line_ids[temp_count])
                    line_ids.append(dpg.generate_uuid())
                    temp_count += 1
                    length -= spacing

                else:
                    if temp_count % 2 == 0:
                        second_point[0] += spacing * math.sin(angle)
                        second_point[1] -= spacing * math.cos(angle)
                        dpg.draw_line(p1=second_point, p2=p2, color=color, thickness=thickness, parent=parent,
                                      id=line_ids[temp_count])
                        line_ids.append(dpg.generate_uuid())
                        temp_count += 1
                    break

                if length >= spacing:
                    first_point = second_point
                    x_co = first_point[0] - spacing * math.sin(angle)
                    y_co = first_point[1] + spacing * math.cos(angle)
                    second_point = [x_co, y_co]
                    first_point = second_point
                    length -= spacing

                else:
                    break


def clear_dot_dashed_line(new_line_flag = 0):
    global line_ids, temp_count
    if new_line_flag == 1:
        line_ids = []
        temp_count = 0
        return

    for id in line_ids:
        if dpg.does_item_exist(item=id):
            dpg.delete_item(item=id)
