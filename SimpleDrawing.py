#-----Import DearPyGui files-----#
from dearpygui.core import *
from dearpygui.simple import *

#-----Import additional modules-----#
from time import sleep
import threading

#-----Import tool scripts-----#
import tools

def pad_mouse_coordinates():
    set_value("##pad_coordinates", get_drawing_mouse_pos())

    #-----Display cross cursor on pad (under development-----#
    temp_count = 0

    delete_draw_command("Pad", f"cursorX {temp_count}")
    delete_draw_command("Pad", f"cursorY {temp_count}")

    mouse_X = get_drawing_mouse_pos()[0]
    mouse_Y = get_drawing_mouse_pos()[1]

    draw_line("Pad", p1=[mouse_X-15, mouse_Y], p2=[mouse_X+15, mouse_Y], color=[100, 100, 100], thickness=2, tag=f"cursorX {temp_count}")
    draw_line("Pad", p1=[mouse_X, mouse_Y-15], p2=[mouse_X, mouse_Y+15], color=[100, 100, 100], thickness=2, tag=f"cursorY {temp_count}")

    temp_count = 1

#-----Running tool scrips again after user is satisfied with their settings-----#
def apply_settings(sender, data):

    if data == "cancel tool":
        delete_item("Tool Specifications", children_only=True)
        add_text("Please select one of the tools from\nthe column on the left to continue\ndrawing.", parent="Tool Specifications")

    if data == "straight line tool":
        tools.straightLineTool("Pad", get_value("Color"), get_value("Thickness"))

    if data == "polyline tool":
        tools.polylineTool("Pad", get_value("Color"), get_value("Thickness"))

    if data == "doodle tool":
        tools.doodleTool("Pad", get_value("Color"), get_value("Thickness"))

#-----Setting up a new thread for running the tool scripts-----#
def apply_settings_dispatcher(sender, data):
    settingsThread = threading.Thread(name="toolSettingsCallbackThread", target=apply_settings, args=(sender, data, ), daemon=True)
    settingsThread.start()

#-----Running scripts when buttons are clicked-----#
def tool_callbacks(caller_button):
    if caller_button == "reset tool":
        delete_item("Tool Specifications", children_only=True)
        add_text("Drawing pad has been erased.\n\nTo get started, please select one of\nthe tools from the column on the\nleft.", parent="Tool Specifications")
        tools.resetPad("Pad")

    if caller_button == "straight line tool":
        #-----Setting up the properties column-----#

        delete_item("Tool Specifications", children_only=True)

        add_spacing(count=1, parent="Tool Specifications")
        add_text("        Straight Line Tool Properties", parent="Tool Specifications")
        add_spacing(count=3, parent="Tool Specifications")
        add_separator(parent="Tool Specifications")
        add_spacing(count=1, parent="Tool Specifications")

        with child("tool properties", height=100, parent="Tool Specifications"):
            add_spacing(count=2)
            add_input_int("Thickness", default_value=5, min_value=1, max_value=100, width=145)
            add_spacing(count=2)
            add_color_edit3("Color", default_value=[0, 255, 255, 255])

        add_button("Cancel", parent="Tool Specifications", height=30, width=110)
        add_same_line(spacing=8.0, parent="Tool Specifications")
        add_button("Apply", parent="Tool Specifications", height=30, width=110)
        add_spacing(count=1, parent="Tool Specifications")
        add_separator(parent="Tool Specifications")

        add_spacing(count=2, parent="Tool Specifications")
        add_text("How to use: ", parent="Tool Specifications")
        add_text("Left click on the drawing pad to set\nthe first point. Then left click again to\nend the line tool.", parent="Tool Specifications")

        set_item_callback("Apply", callback=apply_settings_dispatcher, callback_data="straight line tool")
        set_item_callback("Cancel", callback=apply_settings_dispatcher, callback_data="cancel tool")

        #-----Straight line main function call-----#
        tools.straightLineTool("Pad", get_value("Color"), get_value("Thickness"))

    if caller_button == "polyline tool":
        # -----Setting up the properties column-----#
        delete_item("Tool Specifications", children_only=True)
        add_spacing(count=1, parent="Tool Specifications")
        add_text("            Polyline Tool Properties", parent="Tool Specifications")
        add_spacing(count=3, parent="Tool Specifications")
        add_separator(parent="Tool Specifications")
        add_spacing(count=1, parent="Tool Specifications")

        with child("tool properties", height=100, parent="Tool Specifications"):
            add_spacing(count=2)
            add_input_int("Thickness", default_value=5, min_value=1, max_value=100, width=145)
            add_spacing(count=2)
            add_color_edit3("Color", default_value=[0, 255, 255, 255])

        add_button("Cancel", parent="Tool Specifications", height=30, width=110)
        add_same_line(spacing=8.0, parent="Tool Specifications")
        add_button("Apply", parent="Tool Specifications", height=30, width=110)
        add_spacing(count=1, parent="Tool Specifications")
        add_separator(parent="Tool Specifications")

        add_spacing(count=2, parent="Tool Specifications")
        add_text("How to use: ", parent="Tool Specifications")
        add_text("Left click on the drawing pad to set\nthe first point. Then left click again to\nend the line tool.", parent="Tool Specifications")

        set_item_callback("Apply", callback=apply_settings_dispatcher, callback_data="polyline tool")
        set_item_callback("Cancel", callback=apply_settings_dispatcher, callback_data="cancel tool")

        # -----Polyline main function call-----#
        tools.polylineTool("Pad", get_value("Color"), get_value("Thickness"))

    if caller_button == "doodle tool":
        # -----Setting up the properties column-----#
        delete_item("Tool Specifications", children_only=True)
        add_spacing(count=1, parent="Tool Specifications")
        add_text("            Doodle Tool Properties", parent="Tool Specifications")
        add_spacing(count=3, parent="Tool Specifications")
        add_separator(parent="Tool Specifications")
        add_spacing(count=1, parent="Tool Specifications")

        with child("tool properties", height=100, parent="Tool Specifications"):
            add_spacing(count=2)
            add_input_int("Thickness", default_value=5, min_value=1, max_value=100, width=145)
            add_spacing(count=2)
            add_color_edit3("Color", default_value=[0, 255, 255, 255])

        add_button("Cancel", parent="Tool Specifications", height=30, width=110)
        add_same_line(spacing=8.0, parent="Tool Specifications")
        add_button("Apply", parent="Tool Specifications", height=30, width=110)
        add_spacing(count=1, parent="Tool Specifications")
        add_separator(parent="Tool Specifications")

        add_spacing(count=2, parent="Tool Specifications")
        add_text("How to use: ", parent="Tool Specifications")
        add_text("Left click on the drawing pad to set\nthe first point. Then left click again to\nend the line tool.", parent="Tool Specifications")

        set_item_callback("Apply", callback=apply_settings_dispatcher, callback_data="doodle tool")
        set_item_callback("Cancel", callback=apply_settings_dispatcher, callback_data="cancel tool")

        # -----Doodle main function call-----#
        tools.doodleTool("Pad", get_value("Color"), get_value("Thickness"))

#-----Setting up a new thread for running the tool scripts-----#
def tool_callback_dispatcher(sender):
    toolThread = threading.Thread(name="toolCallbackThread", target=tool_callbacks, args=(sender, ), daemon=True)
    toolThread.start()

#-----Main Window widget-----#
with window("Main Window"):

    #-----Main Window styling-----#
    set_main_window_title("SimpleDrawing")
    set_main_window_pos(x=0, y=0)
    set_main_window_size(width=1370, height=740)
    add_additional_font("fonts/OpenSans-Regular.ttf", 18)

    #set_style_window_padding(0.00, 0.00)
    set_style_item_spacing(0.00, 5.00)
    set_style_item_inner_spacing(0.00, 0.00)
    set_style_touch_extra_padding(0.00, 0.00)
    set_style_window_border_size(0.00)
    set_style_window_rounding(0.00)
    set_style_window_title_align(0.50, 0.50)

    #-----Main Window colors-----#
    set_theme("Light")
    set_theme_item(mvGuiCol_Border, 100, 100, 100, 70)
    set_item_color("Main Window", color=[225, 225, 225], style=mvGuiCol_WindowBg)

#-----Tools window widget-----#
with window("Tools", no_collapse=True, no_resize=True, no_move=True, no_close=True, x_pos=0, y_pos=0, width=70, height=1370):

    #-----Tool Bar window styling-----#
    set_item_color("Tools", color=[225, 225, 225], style=mvGuiCol_WindowBg)
    set_item_color("Tools", color=[225, 225, 225], style=mvGuiCol_TitleBg)
    set_item_color("Tools", color=[225, 225, 225], style=mvGuiCol_TitleBgActive)
    set_item_color("Tools", color=[225, 225, 225], style=mvGuiCol_Button)
    set_item_color("Tools", color=[200, 200, 200], style=mvGuiCol_ButtonHovered)
    set_item_color("Tools", color=[200, 200, 200], style=mvGuiCol_ButtonActive)

    set_style_window_padding(8, 8)
    set_style_frame_border_size(1.0)
    #set_item_style_var("Tools", style=mvGuiStyleVar_FramePadding, value=[0, 5])
    set_item_style_var("Tools", style=mvGuiStyleVar_FrameRounding, value=[12])

    #-----General sketching tool buttons-----#
    add_image_button(name="straight line tool", value="icons/straight-line-tool.png", width=45, height=45, frame_padding=5, tip="Straight line tool", callback=tool_callback_dispatcher)
    add_spacing(count=1)
    add_image_button(name="polyline tool", value="icons/polyline-tool.png", width=45, height=45, frame_padding=5, tip="Polyline tool", callback=tool_callback_dispatcher)
    add_spacing(count=1)
    add_image_button(name="doodle tool", value="icons/doodle-tool.png", width=45, height=45, frame_padding=5, tip="Doodle tool", callback=tool_callback_dispatcher)
    add_spacing(count=1)
    add_image_button(name="rectangle tool", value="icons/rectangle-tool.png", width=45, height=45, frame_padding=5, tip="Rectangle tool")
    add_spacing(count=1)
    add_image_button(name="circle tool", value="icons/circle-tool.png", width=45, height=45, frame_padding=5, tip="Circle tool")
    add_spacing(count=1)
    add_separator()
    add_spacing(count=1)
    add_image_button(name="reset tool", value="icons/reset-tool.png", width=45, height=45, frame_padding=5, tip="Reset entire drawing pad", callback=tool_callbacks)

#-----Tool Specifications window widget-----#
with window("Tool Specifications", no_collapse=True, no_resize=True, no_move=True, no_close=True, x_pos=70, y_pos=0, width=245, height=669):

    #-----Tool Specifications window styling-----#
    set_item_color("Tool Specifications", color=[240, 240, 240], style=mvGuiCol_WindowBg)
    set_item_color("Tool Specifications", color=[240, 240, 240], style=mvGuiCol_TitleBg)
    set_item_color("Tool Specifications", color=[240, 240, 240], style=mvGuiCol_TitleBgActive)
    set_item_color("Tool Specifications", color=[240, 240, 240], style=mvGuiCol_Button)
    set_item_color("Tool Specifications", color=[200, 200, 200], style=mvGuiCol_ButtonHovered)
    set_item_color("Tool Specifications", color=[200, 200, 200], style=mvGuiCol_ButtonActive)
    set_item_color("Tool Specifications", color=[230, 230, 230], style=mvGuiCol_FrameBg)
    set_item_color("Tool Specifications", color=[210, 210, 210], style=mvGuiCol_FrameBgHovered)
    set_item_color("Tool Specifications", color=[210, 210, 210], style=mvGuiCol_FrameBgActive)
    set_item_color("Tool Specifications", color=[250, 250, 250], style=mvGuiCol_ChildBg)

    set_item_style_var("Tool Specifications", style=mvGuiStyleVar_ItemInnerSpacing, value=[5, 0])
    set_item_style_var("Tool Specifications", style=mvGuiStyleVar_FrameRounding, value=[2.0])
    set_item_style_var("Tool Specifications", style=mvGuiStyleVar_ChildBorderSize, value=[1])
    set_item_style_var("Tool Specifications", style=mvGuiStyleVar_ChildRounding, value=[5])

    add_text("To get started, please select one of\nthe tools from the column on the\nleft.")

#----Drawing Pad window widget----#
with window("Drawing Pad", no_close=True, no_collapse=True, no_resize=True, x_pos=315, y_pos=0, autosize=True, no_move=True):

    #-----Drawing Pad window styling-----#
    set_item_color("Drawing Pad", color=[255, 255, 255], style=mvGuiCol_WindowBg)
    set_item_color("Drawing Pad", color=[255, 255, 255], style=mvGuiCol_TitleBg)
    set_item_color("Drawing Pad", color=[255, 255, 255], style=mvGuiCol_TitleBgActive)

    #-----Adding drawing canvas-----#
    add_drawing("Pad", height=629, width=1065)

#-----Window to display mosue coordinates-----#
with window("Mouse Pad Coordinates", no_close=True, no_collapse=True, no_resize=True, no_title_bar=True, x_pos=1130, y_pos=670, no_move=True, height=50, width=250):
    set_item_color("Mouse Pad Coordinates", color=[225, 225, 225], style=mvGuiCol_WindowBg)
    add_text("Mouse coordinates:", color=[100, 100, 100])
    add_same_line(spacing=4)
    add_label_text("##pad_coordinates", default_value="(0,0)", color=[100, 100, 100])

#-----Window to display SimpleDrawing version number-----#
with window("SimpleDrawing Name", no_close=True, no_collapse=True, no_resize=True, no_title_bar=True, x_pos=60, y_pos=670, no_move=True, height=50, width=350):
    set_item_color("SimpleDrawing Name", color=[225, 225, 225], style=mvGuiCol_WindowBg)
    add_text("SimpleDrawing", color=[100, 100, 100])
    add_same_line(spacing=4)

#-----Window to credit Dear PyGui-----#
with window("DPG", no_close=True, no_collapse=True, no_resize=True, no_title_bar=True, x_pos=310, y_pos=670, no_move=True, height=50, width=350):
    set_item_color("DPG", color=[225, 225, 225], style=mvGuiCol_WindowBg)
    add_text("Powered by Dear PyGui", color=[100, 100, 100])
    add_same_line(spacing=4)

set_mouse_move_callback(pad_mouse_coordinates)

#-----Start app-----#
start_dearpygui(primary_window="Main Window")
