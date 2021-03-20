from dearpygui.core import *
import sqlite3
import tools
import shutil
import os

row_count = 0
row_pointer = 0

def create_db():
    conn = sqlite3.connect("SimpleDrawingTemp_db.db")
    c = conn.cursor()

    c.execute("""drop table if exists SimpleDrawingTools""")

    c.execute("""CREATE TABLE SimpleDrawingTools (
                    RowID int,
                    Tool text,
                    Point_1 text,
                    Point_2 text,
                    Point_3 text,
                    Point_4 text,
                    Color text,
                    CanvasBefore text,
                    CanvasAfter text,
                    Thickness real,
                    Spacing real,
                    Fill text,
                    Rounding real,
                    Size real,
                    Text text,
                    Image text,
                    Tag text)""")

    conn.commit()
    conn.close()


def write_db(tool: str, point_1='', point_2='', point_3='', point_4='', color='', canvasBefore='', canvasAfter='',
             thickness=0.0, spacing=0.0, fill='', rounding=0.0, size=0.0, text='', image='', tag=''):

    global row_count, canvasColorBefore, row_pointer, flag

    row_count += 1
    row_pointer += 1

    conn = sqlite3.connect("SimpleDrawingTemp_db.db")
    c = conn.cursor()

    if row_pointer != row_count:
        for row in range(row_pointer, row_count):
            c.execute(f"DELETE FROM SimpleDrawingTools WHERE RowID={row}")

        if row_pointer == 1:
            canvasColorBefore = '[255, 255, 255, 255]'
        else:
            canvasColorBefore = c.execute(f"SELECT CanvasBefore FROM SimpleDrawingTools WHERE Tool='canvas color tool'")
            canvasColorBefore = c.fetchall()
            if canvasColorBefore != []:
                canvasColorBefore = canvasColorBefore[-1]
                canvasColorBefore = canvasColorBefore[0]

        row_count = row_pointer
        flag = 1

    else:
        flag = 0

    if tool == "straight line tool":
        c.execute("""INSERT INTO SimpleDrawingTools (RowID, Tool, Point_1, Point_2, Color, Thickness, Tag)
        VALUES (?, ?, ?, ?, ?, ?, ?)""", (row_count, tool, point_1, point_2, color, thickness, tag))

    elif tool == "dashed line tool":
        c.execute("""INSERT INTO SimpleDrawingTools (RowID, Tool, Point_1, Point_2, Color, Thickness, Spacing, Tag)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (row_count, tool, point_1, point_2, color, thickness, spacing, tag))

    elif tool == "polyline tool":
        c.execute("""INSERT INTO SimpleDrawingTools (RowID, Tool, Point_1, Point_2, Color, Thickness, Tag)
           VALUES (?, ?, ?, ?, ?, ?, ?)""", (row_count, tool, point_1, point_2, color, thickness, tag))

    elif tool == "doodle tool":
        c.execute("""INSERT INTO SimpleDrawingTools (RowID, Tool, Point_1, Color, Thickness, Tag)
           VALUES (?, ?, ?, ?, ?, ?)""", (row_count, tool, point_1, color, thickness, tag))

    elif tool == "rectangle tool":
        c.execute("""INSERT INTO SimpleDrawingTools (RowID, Tool, Point_1, Point_2, Color, Thickness, Fill, Rounding, Tag)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", (row_count, tool, point_1, point_2, color, thickness, fill, rounding, tag))

    elif tool == "circle tool":
        c.execute("""INSERT INTO SimpleDrawingTools (RowID, Tool, Point_1, Point_2, Color, Thickness, Fill, Tag)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (row_count, tool, point_1, point_2, color, thickness, fill, tag))

    elif tool == "arrow tool":
        c.execute("""INSERT INTO SimpleDrawingTools (RowID, Tool, Point_1, Point_2, Color, Thickness, Size, Tag)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (row_count, tool, point_1, point_2, color, thickness, size, tag))

    elif tool == "bezier tool":
        c.execute("""INSERT INTO SimpleDrawingTools (RowID, Tool, Point_1, Point_2, Point_3, Point_4, Color, Thickness, Tag)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", (row_count, tool, point_1, point_2, point_3, point_4, color, thickness, tag))

    elif tool == "text tool":
        c.execute("""INSERT INTO SimpleDrawingTools (RowID, Tool, Point_1, Color, Size, Text, Tag)
        VALUES (?, ?, ?, ?, ?, ?, ?)""", (row_count, tool, point_1, color, size, text, tag))

    elif tool == "canvas color tool":
        c.execute("""INSERT INTO SimpleDrawingTools (RowID, Tool, CanvasBefore, CanvasAfter)
        VALUES (?, ?, ?, ?)""", (row_count, tool, canvasBefore, canvasAfter))

    elif tool == "image tool":
        c.execute("""INSERT INTO SimpleDrawingTools (RowID, Tool, Point_1, Point_2, Image, Tag)
        VALUES (?, ?, ?, ?, ?, ?)""", (row_count, tool, point_1, point_2, image, tag))

        if flag == 1:
            c.execute(f"UPDATE SimpleDrawingTools SET CanvasBefore = '{canvasColorBefore}' WHERE RowID = {row_count}")

    conn.commit()
    conn.close()

def readAll_db():
    conn = sqlite3.connect("SimpleDrawingTemp_db.db")
    c = conn.cursor()

    c.execute("SELECT * FROM SimpleDrawingTools")

    for row in c.fetchall():
        print(row)

    conn.close()

def read_db(action: str):
    global row_count
    global row_pointer

    conn = sqlite3.connect("SimpleDrawingTemp_db.db")
    c = conn.cursor()

    if action == "undo":
        if row_pointer == 0:
            set_item_color("Drawing Pad", style=mvGuiCol_WindowBg, color=[255, 255, 255, 255])
            return

        tool = c.execute(f"SELECT Tool FROM SimpleDrawingTools WHERE RowID={row_pointer}")
        tool = c.fetchone()
        tool = tool[0]

        if tool == 'canvas color tool':
            canvasColor = c.execute(f"SELECT CanvasBefore FROM SimpleDrawingTools WHERE RowID='{row_pointer}'")
            canvasColor = c.fetchone()[0]
            canvasColor = string_to_list(canvasColor)
            set_item_color("Drawing Pad", style=mvGuiCol_WindowBg, color=canvasColor)
            row_pointer -= 1

        elif tool == 'dashed line tool':
            tag = c.execute(f"SELECT Tag FROM SimpleDrawingTools WHERE RowID={row_pointer}")
            tag = c.fetchone()[0]
            tools.clear_dashed_line(drawing="Pad", tag=tag)
            row_pointer -= 1

        else:
            tag = c.execute(f"SELECT Tag FROM SimpleDrawingTools WHERE RowID={row_pointer}")
            tag = c.fetchone()[0]
            delete_draw_command("Pad", tag)
            row_pointer -= 1

    elif action == "redo":
        if row_pointer == row_count:
            return

        row_pointer += 1

        tool = c.execute(f"SELECT Tool FROM SimpleDrawingTools WHERE RowID={row_pointer}")
        tool = c.fetchone()
        tool = tool[0]

        if tool == 'canvas color tool':
            canvasColor = c.execute(f"SELECT CanvasAfter FROM SimpleDrawingTools WHERE RowID='{row_pointer}'")
            canvasColor = c.fetchone()[0]
            canvasColor = string_to_list(canvasColor)
            set_item_color("Drawing Pad", style=mvGuiCol_WindowBg, color=canvasColor)

        elif tool == 'straight line tool' or tool == 'polyline tool':
            toolInfo = c.execute(f"SELECT Point_1, Point_2, Color, Thickness, Tag FROM SimpleDrawingTools WHERE RowID={row_pointer}")
            toolInfo = c.fetchone()
            draw_line("Pad", p1=string_to_list(toolInfo[0]), p2=string_to_list(toolInfo[1]), color=string_to_list(toolInfo[2]), thickness=int(toolInfo[3]), tag=toolInfo[4])

        elif tool == 'dashed line tool':
            toolInfo = c.execute(f"SELECT Point_1, Point_2, Color, Thickness, Spacing, Tag FROM SimpleDrawingTools WHERE RowID={row_pointer}")
            toolInfo = c.fetchone()
            tools.draw_dashed_line("Pad", p1=string_to_list(toolInfo[0]), p2=string_to_list(toolInfo[1]), color=string_to_list(toolInfo[2]), thickness=int(toolInfo[3]), spacing=toolInfo[4], tag=toolInfo[5])

        elif tool == 'doodle tool':
            toolInfo = c.execute(f"SELECT  Point_1, Color, Thickness, Tag FROM SimpleDrawingTools WHERE RowID={row_pointer}")
            toolInfo = c.fetchone()
            draw_polyline("Pad", points=string_to_list(toolInfo[0], dashed=True), color=string_to_list(toolInfo[1]), thickness=int(toolInfo[2]), tag=toolInfo[3])

        elif tool == 'rectangle tool':
            toolInfo = c.execute(f"SELECT Point_1, Point_2, Color, Thickness, Fill, Rounding, Tag FROM SimpleDrawingTools WHERE RowID={row_pointer}")
            toolInfo = c.fetchone()
            draw_rectangle("Pad", pmin=string_to_list(toolInfo[0]), pmax=string_to_list(toolInfo[1]), color=string_to_list(toolInfo[2]), thickness=float(toolInfo[3]), fill=string_to_list(toolInfo[4]), rounding=float(toolInfo[5]), tag=toolInfo[6])

        elif tool == 'circle tool':
            toolInfo = c.execute(f"SELECT Point_1, Point_2, Color, Thickness, Fill, Tag FROM SimpleDrawingTools WHERE RowID={row_pointer}")
            toolInfo = c.fetchone()
            draw_circle("Pad", center=string_to_list(toolInfo[0]), radius=float(toolInfo[1]), color=string_to_list(toolInfo[2]), thickness=float(toolInfo[3]), fill=string_to_list(toolInfo[4]), tag=toolInfo[5])

        elif tool == 'arrow tool':
            toolInfo = c.execute(f"SELECT Point_1, Point_2, Color, Thickness, Size, Tag FROM SimpleDrawingTools WHERE RowID={row_pointer}")
            toolInfo = c.fetchone()
            draw_arrow("Pad", p1=string_to_list(toolInfo[0]), p2=string_to_list(toolInfo[1]), color=string_to_list(toolInfo[2]), thickness=int(toolInfo[3]), size=int(toolInfo[4]), tag=toolInfo[5])

        elif tool == 'bezier tool':
            toolInfo = c.execute(f"SELECT Point_1, Point_2, Point_3, Point_4, Color, Thickness, Tag FROM SimpleDrawingTools WHERE RowID={row_pointer}")
            toolInfo = c.fetchone()
            draw_bezier_curve("Pad", p1=string_to_list(toolInfo[0]), p2=string_to_list(toolInfo[1]), p3=string_to_list(toolInfo[2]), p4=string_to_list(toolInfo[3]), color=string_to_list(toolInfo[4]), thickness=int(toolInfo[5]), tag=toolInfo[6])

        elif tool == 'text tool':
            toolInfo = c.execute(f"SELECT Point_1, Color, Size, Text, Tag FROM SimpleDrawingTools WHERE RowID={row_pointer}")
            toolInfo = c.fetchone()
            draw_text("Pad", pos=string_to_list(toolInfo[0]), color=string_to_list(toolInfo[1]), size=int(toolInfo[2]), text=toolInfo[3], tag=toolInfo[4])

        elif tool == 'image tool':
            toolInfo = c.execute(f"SELECT Point_1, Point_2, Image, Tag FROM SimpleDrawingTools WHERE RowID={row_pointer}")
            toolInfo = c.fetchone()
            draw_image("Pad", pmin=string_to_list(toolInfo[0]), pmax=string_to_list(toolInfo[1]), file=toolInfo[2], tag=toolInfo[3])

    conn.close()

def open_db(filepath):

    global row_count, row_pointer

    os.remove("SimpleDrawingTemp_db.db")

    original = filepath
    target = os.path.abspath("SimpleDrawingTemp_db.db")
    shutil.copyfile(original, target)

    clear_drawing("Pad")

    conn = sqlite3.connect("SimpleDrawingTemp_db.db")
    c = conn.cursor()

    c.execute("SELECT RowID FROM SimpleDrawingTools")

    for row in c.fetchall():
        row = row[0]
        tool = c.execute(f"SELECT Tool FROM SimpleDrawingTools WHERE RowID={row}")
        tool = c.fetchone()
        tool = tool[0]

        if tool == 'canvas color tool':
            canvasColor = c.execute(f"SELECT CanvasAfter FROM SimpleDrawingTools WHERE RowID='{row}'")
            canvasColor = c.fetchone()[0]
            canvasColor = string_to_list(canvasColor)
            set_item_color("Drawing Pad", style=mvGuiCol_WindowBg, color=canvasColor)

        elif tool == 'straight line tool':
            toolInfo = c.execute(
                f"SELECT Point_1, Point_2, Color, Thickness, Tag FROM SimpleDrawingTools WHERE RowID={row}")
            toolInfo = c.fetchone()
            draw_line("Pad", p1=string_to_list(toolInfo[0]), p2=string_to_list(toolInfo[1]),
                      color=string_to_list(toolInfo[2]), thickness=int(toolInfo[3]), tag=toolInfo[4])

            tools.straight_line_count = int(toolInfo[4][-1]) + 1

        elif tool == 'polyline tool':
            toolInfo = c.execute(
                f"SELECT Point_1, Point_2, Color, Thickness, Tag FROM SimpleDrawingTools WHERE RowID={row}")
            toolInfo = c.fetchone()

            draw_line("Pad", p1=string_to_list(toolInfo[0]), p2=string_to_list(toolInfo[1]),
                      color=string_to_list(toolInfo[2]), thickness=int(toolInfo[3]), tag=toolInfo[4])
            tools.polyline_count = int(toolInfo[4][-1]) + 1

        elif tool == 'dashed line tool':
            toolInfo = c.execute(
                f"SELECT Point_1, Point_2, Color, Thickness, Spacing, Tag FROM SimpleDrawingTools WHERE RowID={row}")
            toolInfo = c.fetchone()

            tools.draw_dashed_line("Pad", p1=string_to_list(toolInfo[0]), p2=string_to_list(toolInfo[1]),
                                   color=string_to_list(toolInfo[2]), thickness=int(toolInfo[3]), spacing=toolInfo[4],
                                   tag=toolInfo[5])

            tools.dashed_line_count = int(toolInfo[5][-1]) + 1

        elif tool == 'doodle tool':
            toolInfo = c.execute(
                f"SELECT  Point_1, Color, Thickness, Tag FROM SimpleDrawingTools WHERE RowID={row}")
            toolInfo = c.fetchone()

            draw_polyline("Pad", points=string_to_list(toolInfo[0], dashed=True), color=string_to_list(toolInfo[1]),
                          thickness=int(toolInfo[2]), tag=toolInfo[3])

            tools.doodle_count = int(toolInfo[3][-1]) + 1

        elif tool == 'rectangle tool':
            toolInfo = c.execute(
                f"SELECT Point_1, Point_2, Color, Thickness, Fill, Rounding, Tag FROM SimpleDrawingTools WHERE RowID={row}")
            toolInfo = c.fetchone()

            draw_rectangle("Pad", pmin=string_to_list(toolInfo[0]), pmax=string_to_list(toolInfo[1]),
                           color=string_to_list(toolInfo[2]), thickness=float(toolInfo[3]),
                           fill=string_to_list(toolInfo[4]), rounding=float(toolInfo[5]), tag=toolInfo[6])

            tools.rectangle_count = int(toolInfo[6][-1]) + 1

        elif tool == 'circle tool':
            toolInfo = c.execute(
                f"SELECT Point_1, Point_2, Color, Thickness, Fill, Tag FROM SimpleDrawingTools WHERE RowID={row}")
            toolInfo = c.fetchone()

            draw_circle("Pad", center=string_to_list(toolInfo[0]), radius=float(toolInfo[1]),
                        color=string_to_list(toolInfo[2]), thickness=float(toolInfo[3]), fill=string_to_list(toolInfo[4]),
                        tag=toolInfo[5])

            tools.circle_count = int(toolInfo[5][-1]) + 1

        elif tool == 'arrow tool':
            toolInfo = c.execute(
                f"SELECT Point_1, Point_2, Color, Thickness, Size, Tag FROM SimpleDrawingTools WHERE RowID={row}")
            toolInfo = c.fetchone()

            draw_arrow("Pad", p1=string_to_list(toolInfo[0]), p2=string_to_list(toolInfo[1]),
                       color=string_to_list(toolInfo[2]), thickness=int(toolInfo[3]), size=int(toolInfo[4]),
                       tag=toolInfo[5])

            tools.arrow_count = int(toolInfo[5][-1]) + 1

        elif tool == 'bezier tool':
            toolInfo = c.execute(
                f"SELECT Point_1, Point_2, Point_3, Point_4, Color, Thickness, Tag FROM SimpleDrawingTools WHERE RowID={row}")
            toolInfo = c.fetchone()

            draw_bezier_curve("Pad", p1=string_to_list(toolInfo[0]), p2=string_to_list(toolInfo[1]),
                              p3=string_to_list(toolInfo[2]), p4=string_to_list(toolInfo[3]),
                              color=string_to_list(toolInfo[4]), thickness=int(toolInfo[5]), tag=toolInfo[6])

            tools.bezier_count = int(toolInfo[6][-1]) + 1

        elif tool == 'text tool':
            toolInfo = c.execute(
                f"SELECT Point_1, Color, Size, Text, Tag FROM SimpleDrawingTools WHERE RowID={row}")
            toolInfo = c.fetchone()

            draw_text("Pad", pos=string_to_list(toolInfo[0]), color=string_to_list(toolInfo[1]), size=int(toolInfo[2]),
                      text=toolInfo[3], tag=toolInfo[4])

            tools.text_count = int(toolInfo[4][-1]) + 1

        elif tool == 'image tool':
            toolInfo = c.execute(f"SELECT Point_1, Point_2, Image, Tag FROM SimpleDrawingTools WHERE RowID={row}")
            toolInfo = c.fetchone()
            draw_image("Pad", pmin=string_to_list(toolInfo[0]), pmax=string_to_list(toolInfo[1]), file=toolInfo[2], tag=toolInfo[3])

        row_count = row
        row_pointer = row

    conn.close()


def string_to_list(string, dashed=False):
    if dashed == False:
        string = list(string[1:-1].split(", "))
        string = [float(num) for num in string]
        return string

    if dashed == True:
        string = list(string[2:-2].split('], ['))

        for i in range (len(string)):
            string[i] = list(string[i].split(", "))
            for j in range(2):
                string[i][j] = float(string[i][j])

        return string

def saveDatabase(filepath):
    original = os.path.abspath("SimpleDrawingTemp_db.db")
    target = filepath
    shutil.copyfile(original, target)


def reset_db():
    global row_pointer
    global row_count

    os.remove("SimpleDrawingTemp_db.db")

    conn = sqlite3.connect("SimpleDrawingTemp_db.db")
    c = conn.cursor()

    c.execute("""CREATE TABLE SimpleDrawingTools (
                        RowID int,
                        Tool text,
                        Point_1 text,
                        Point_2 text,
                        Point_3 text,
                        Point_4 text,
                        Color text,
                        CanvasBefore text,
                        CanvasAfter text,
                        Thickness real,
                        Spacing real,
                        Fill text,
                        Rounding real,
                        Size real,
                        Text text,
                        Tag text)""")

    conn.commit()
    conn.close()

    row_count = 0
    row_pointer = 0

    tools.straight_line_count = 1
    tools.dashed_line_count = 1
    tools.polyline_count = 1
    tools.doodle_count = 1
    tools.rectangle_count = 1
    tools.circle_count = 1
    tools.arrow_count = 1
    tools.bezier_count = 1
    tools.text_count = 1