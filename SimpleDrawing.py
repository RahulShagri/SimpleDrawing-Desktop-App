# Import DearPyGui files
from dearpygui.core import *
from dearpygui.simple import *

# Import additional modules
import threading
import webbrowser

# Import dependent scripts
import tools
from db_manage import *

# Importing Tool Specifications Template Class
from ToolSpecTemplate import *

# Open given URL
def open_website(sender, data):
    webbrowser.open(data)

# To display mouse coordinates on the bottom right corner and cursor following the mouse on the drawing pad
def pad_mouse_coordinates():
    set_value("Mouse coordinates:", f"Mouse coordinates: {get_drawing_mouse_pos()}")

    # Display cross cursor on pad
    delete_draw_command("Pad", f"cursorX")
    delete_draw_command("Pad", f"cursorY")

    mouse_x = get_drawing_mouse_pos()[0]
    mouse_y = get_drawing_mouse_pos()[1]

    draw_line("Pad", p1=[mouse_x - 15, mouse_y], p2=[mouse_x + 15, mouse_y], color=[100, 100, 100], thickness=2,
              tag="cursorX")
    draw_line("Pad", p1=[mouse_x, mouse_y - 15], p2=[mouse_x, mouse_y + 15], color=[100, 100, 100], thickness=2,
              tag="cursorY")

# Running tool scrips again after user is satisfied with their settings
def apply_settings(sender, data):
    if data == "cancel tool":
        delete_item("Tool Specifications", children_only=True)
        add_text("Please select one of the tools from\nthe column on the left to continue\ndrawing.",
                 parent="Tool Specifications")

    if data == "canvas color tool":
        tools.canvasColorTool("Drawing Pad", get_value("Color"))

    if data == "straight line tool":
        tools.straightLineTool("Pad", get_value("Color"), get_value("Thickness"))

    if data == "polyline tool":
        tools.polylineTool("Pad", get_value("Color"), get_value("Thickness"))

    if data == "doodle tool":
        tools.doodleTool("Pad", get_value("Color"), get_value("Thickness"))

    if data == "rectangle tool":
        if get_value("Fill rectangle"):
            if get_value("Fill with same color"):
                tools.rectangleTool("Pad", get_value("Color"), get_value("Thickness"), get_value("Rounding"), get_value("Color"))
            else:
                tools.rectangleTool("Pad", get_value("Color"), get_value("Thickness"), get_value("Rounding"), get_value("Fill color"))
        else:
            tools.rectangleTool("Pad", get_value("Color"), get_value("Thickness"), get_value("Rounding"), [0, 0, 0, 0])

    if data == "circle tool":
        if get_value("Fill circle"):
            if get_value("Fill with same color"):
                tools.circleTool("Pad", get_value("Color"), get_value("Thickness"), get_value("Color"))
            else:
                tools.circleTool("Pad", get_value("Color"), get_value("Thickness"), get_value("Fill color"))
        else:
            tools.circleTool("Pad", get_value("Color"), get_value("Thickness"), [0, 0, 0, 0])

    if data == "arrow tool":
        tools.arrowTool("Pad", get_value("Color"), get_value("Thickness"), get_value("Arrow size"))

    if data == "bezier tool":
        tools.bezierTool("Pad", get_value("Color"), get_value("Thickness"))

    if data == "dashed line tool":
        tools.dashedLineTool("Pad", get_value("Color"), get_value("Thickness"), get_value("Spacing"))

    if data == "text tool":
        tools.textTool("Pad", get_value("Text"), get_value("Color"), get_value("Size"))

    if data == 'image tool':
        if get_value("##imagePath") != "Please select an image.":
            tools.imageTool("Pad", get_value("##imagePath"))

# Setting up a new thread for running the tool scripts
def apply_settings_dispatcher(sender, data):
    settings_thread = threading.Thread(name="toolSettingsCallbackThread", target=apply_settings, args=(sender, data,),
                                       daemon=True)
    settings_thread.start()

# Running scripts when buttons are clicked
def tool_callbacks(caller_button):

    if caller_button == "No##reset":
        close_popup("Are you sure you want to erase the drawing pad?")

    if caller_button == "Yes##reset":
        close_popup("Are you sure you want to erase the drawing pad?")
        delete_item("Tool Specifications", children_only=True)
        add_text(
            "Drawing pad has been erased."
            "\n\nTo get started, please select one of"
            "\nthe tools from the column on the"
            "\nleft.",
            parent="Tool Specifications")
        tools.resetPad("Pad")

    if caller_button == "canvas color tool":
        # Setting up the properties column
        delete_item("Tool Specifications", children_only=True)

        canvas_color_specifications = ToolSpec(title="               Change canvas color", height=230)

        add_color_picker3("Color", default_value=[255, 255, 255], parent="tool properties", width=140)

        set_item_callback("Apply", callback=apply_settings_dispatcher, callback_data="canvas color tool")
        set_item_callback("Cancel", callback=apply_settings_dispatcher, callback_data="cancel tool")

    if caller_button == "straight line tool":
        # Setting up the properties column
        delete_item("Tool Specifications", children_only=True)

        straight_line_specifications = ToolSpec(title="        Straight Line Tool Properties", height=100)

        add_input_int("Thickness", default_value=5, min_value=1, width=145, parent="tool properties")
        straight_line_specifications.add_space(count=2)
        add_color_edit4("Color", default_value=[0, 255, 255, 255], parent="tool properties", width=170)

        straight_line_specifications.add_instructions(value="Left click on the drawing pad to set\n"
                                                            "the first point. Then left click, right\n"
                                                            "click or hit escape key to end the line\n"
                                                            "tool.")

        set_item_callback("Apply", callback=apply_settings_dispatcher, callback_data="straight line tool")
        set_item_callback("Cancel", callback=apply_settings_dispatcher, callback_data="cancel tool")

        # Straight line main function call
        tools.straightLineTool("Pad", get_value("Color"), get_value("Thickness"))

    if caller_button == "dashed line tool":
        # Setting up the properties column
        delete_item("Tool Specifications", children_only=True)

        dashedLine_specifications = ToolSpec(title="          Dashed Line Tool Properties", height=130)

        add_input_int("Thickness", default_value=5, min_value=1, width=145, parent="tool properties")
        dashedLine_specifications.add_space(count=2)
        add_input_int("Spacing", default_value=30, min_value=1, width=145, parent="tool properties")
        dashedLine_specifications.add_space(count=2)
        add_color_edit4("Color", default_value=[0, 255, 255, 255], parent="tool properties", width=170)

        dashedLine_specifications.add_instructions(value="Left click on the drawing pad to set\n"
                                                            "the first point. Then left click, right\n"
                                                            "click or hit escape key to end the line\n"
                                                            "tool.")

        set_item_callback("Apply", callback=apply_settings_dispatcher, callback_data="dashed line tool")
        set_item_callback("Cancel", callback=apply_settings_dispatcher, callback_data="cancel tool")

        # Dashed line main function call
        tools.dashedLineTool("Pad", get_value("Color"), get_value("Thickness"), get_value("Spacing"))

    if caller_button == "polyline tool":
        # Setting up the properties column
        delete_item("Tool Specifications", children_only=True)

        polyline_specifications = ToolSpec(title="            Polyline Tool Properties", height=150)

        add_input_int("Thickness", default_value=5, min_value=1, width=145, parent="tool properties")
        polyline_specifications.add_space(count=2)
        add_color_edit4("Color", default_value=[0, 255, 255, 255], parent="tool properties", width=170)
        polyline_specifications.add_space(count=2)
        polyline_specifications.add_separate()
        polyline_specifications.add_space(count=2)
        add_checkbox("Close polyline", default_value=False, parent="tool properties")

        polyline_specifications.add_instructions(value="Left click on the drawing pad to set\n"
                                                       "the first point. Then left click to add\n"
                                                       "more points. Right click or hit the\n"
                                                       "escape key on the keyboard to end\n"
                                                       "the line tool.\n"
                                                       "\n"
                                                       "If you have selected \"Close polyline\",\n"
                                                       "then the polyline will close when the\n"
                                                       "tool is terminated")

        set_item_callback("Apply", callback=apply_settings_dispatcher, callback_data="polyline tool")
        set_item_callback("Cancel", callback=apply_settings_dispatcher, callback_data="cancel tool")

        # Polyline main function call
        tools.polylineTool("Pad", get_value("Color"), get_value("Thickness"))

    if caller_button == "doodle tool":
        # Setting up the properties column
        delete_item("Tool Specifications", children_only=True)

        doodle_specifications = ToolSpec(title="             Doodle Tool Properties", height=100)

        add_input_int("Thickness", default_value=5, min_value=1, width=145, parent="tool properties")
        doodle_specifications.add_space(count=2)
        add_color_edit4("Color", default_value=[0, 255, 255, 255], parent="tool properties", width=170)

        doodle_specifications.add_instructions(value="Left click on the drawing pad to set\n"
                                                     "the first point. Then left click, to end\n"
                                                     "the tool. Right click or hit escape key\n"
                                                     "to undo the drawn line")


        set_item_callback("Apply", callback=apply_settings_dispatcher, callback_data="doodle tool")
        set_item_callback("Cancel", callback=apply_settings_dispatcher, callback_data="cancel tool")

        # Doodle main function call
        tools.doodleTool("Pad", get_value("Color"), get_value("Thickness"))

    if caller_button == "rectangle tool":
        # Setting up the properties column
        delete_item("Tool Specifications", children_only=True)

        rectangle_specifications = ToolSpec(title="            Rectangle Tool Properties", height=175)

        add_input_float("Thickness", default_value=5, step=1, min_value=1, width=145, parent="tool properties")
        rectangle_specifications.add_space(count=2)
        add_input_float("Rounding", default_value=0, step=1, min_value=0, width=145, parent="tool properties")
        rectangle_specifications.add_space(count=2)
        add_color_edit4("Color", default_value=[0, 255, 255, 255], parent="tool properties", width=170)
        rectangle_specifications.add_space(count=1)
        rectangle_specifications.add_separate()
        rectangle_specifications.add_space(count=1)
        add_checkbox("Fill rectangle", default_value=False, parent="tool properties", callback=tools.fillRectangleCheckbox)

        rectangle_specifications.add_instructions(value="Left click on the drawing pad to set\n"
                                                        "the first point. Then left click to set\n"
                                                        "the second point. Right click or hit\n"
                                                        "escape key to end the tool")

        set_item_callback("Apply", callback=apply_settings_dispatcher, callback_data="rectangle tool")
        set_item_callback("Cancel", callback=apply_settings_dispatcher, callback_data="cancel tool")

        # Doodle main function call
        tools.rectangleTool("Pad", get_value("Color"), get_value("Thickness"), get_value("Rounding"), [0, 0, 0, 0])

    if caller_button == "circle tool":
        # Setting up the properties column
        delete_item("Tool Specifications", children_only=True)

        circle_specifications = ToolSpec(title="            Circle Tool Properties", height=135)

        add_input_float("Thickness", default_value=5, step=1, min_value=1, width=145, parent="tool properties")
        circle_specifications.add_space(count=2)
        add_color_edit4("Color", default_value=[0, 255, 255, 255], parent="tool properties", width=170)
        circle_specifications.add_space(count=1)
        circle_specifications.add_separate()
        circle_specifications.add_space(count=1)
        add_checkbox("Fill circle", default_value=False, parent="tool properties", callback=tools.fillCircleCheckbox)

        circle_specifications.add_instructions(value="Left click on the drawing pad to set\n"
                                                        "the centre point. Then left click to set\n"
                                                        "the radius. Right click or hit\n"
                                                        "escape key to end the tool")

        set_item_callback("Apply", callback=apply_settings_dispatcher, callback_data="circle tool")
        set_item_callback("Cancel", callback=apply_settings_dispatcher, callback_data="cancel tool")

        # Circle main function call
        tools.circleTool("Pad", get_value("Color"), get_value("Thickness"), [0, 0, 0, 0])

    if caller_button == "arrow tool":
        # Setting up the properties column
        delete_item("Tool Specifications", children_only=True)

        arrow_specifications = ToolSpec(title="           Arrow Tool Properties", height=135)

        add_input_int("Thickness", default_value=5, min_value=1, width=145, parent="tool properties")
        arrow_specifications.add_space(count=2)
        add_input_int("Arrow size", default_value=20, min_value=1, width=145, parent="tool properties")
        arrow_specifications.add_space(count=2)
        add_color_edit4("Color", default_value=[0, 255, 255, 255], parent="tool properties", width=170)

        arrow_specifications.add_instructions(value="Left click on the drawing pad to set\n"
                                                            "the first point. Then left click, right\n"
                                                            "click or hit escape key to end the line\n"
                                                            "tool.")

        set_item_callback("Apply", callback=apply_settings_dispatcher, callback_data="arrow tool")
        set_item_callback("Cancel", callback=apply_settings_dispatcher, callback_data="cancel tool")

        # Arrow main function call
        tools.arrowTool("Pad", get_value("Color"), get_value("Thickness"), get_value("Arrow size"))

    if caller_button == "bezier tool":
        # Setting up the properties column
        delete_item("Tool Specifications", children_only=True)

        bezier_specifications = ToolSpec(title="            Bezier Tool Properties", height=150)

        add_input_int("Thickness", default_value=5, min_value=1, width=145, parent="tool properties")
        bezier_specifications.add_space(count=2)
        add_color_edit4("Color", default_value=[0, 255, 255, 255], parent="tool properties", width=170)
        bezier_specifications.add_space(count=2)
        bezier_specifications.add_separate()
        bezier_specifications.add_space(count=2)
        add_checkbox("Close bezier curve", default_value=False, parent="tool properties")

        bezier_specifications.add_instructions(value="Left click on the drawing pad to set\n"
                                                       "the first point. Then left click to add\n"
                                                       "three more points. Right click or hit\n"
                                                       "the escape key on the keyboard to\n"
                                                       "end the tool.\n\n"
                                                     "If you have selected the \"Close bezier\n"
                                                     "curve\" then the bezier curve will close\n"
                                                     "when the third point is selected")

        set_item_callback("Apply", callback=apply_settings_dispatcher, callback_data="bezier tool")
        set_item_callback("Cancel", callback=apply_settings_dispatcher, callback_data="cancel tool")

        # Bezier main function call
        tools.bezierTool("Pad", get_value("Color"), get_value("Thickness"))

    if caller_button == "text tool":
        # Setting up the properties column
        delete_item("Tool Specifications", children_only=True)

        text_specifications = ToolSpec(title="               Text Tool Properties", height=170)

        add_input_text("Text", hint="Enter the text here", multiline=True, parent="tool properties", height=60, width=175)
        text_specifications.add_space(count=2)
        add_input_int("Size", default_value=40, min_value=1, width=145, parent="tool properties")
        text_specifications.add_space(count=2)
        add_color_edit4("Color", default_value=[0, 255, 255, 255], parent="tool properties", width=170)

        text_specifications.add_instructions(value="Left click on the canvas to initiate the\n"
                                                   "text tool. When you are satisfied with\n"
                                                   "the placement, left click again to\n"
                                                   "place the text.\n\n"
                                                   "Right clicking or pressing the escape\n"
                                                   "key will terminate the text tool.")

        set_item_callback("Apply", callback=apply_settings_dispatcher, callback_data="text tool")
        set_item_callback("Cancel", callback=apply_settings_dispatcher, callback_data="cancel tool")

        # Test main function call
        tools.textTool("Pad", "Example Text", get_value("Color"), get_value("Size"))

    if caller_button == "image tool":
        # Setting up the properties column
        delete_item("Tool Specifications", children_only=True)

        image_specifications = ToolSpec(title="               Image Tool Properties", height=105)

        add_button("Search image", parent="tool properties", height=30, width=210, callback=tools.searchImage)
        image_specifications.add_space(count=2)
        add_input_text(name="##imagePath", multiline=True, readonly=True, parent="tool properties", height=25, width=210)
        set_value("##imagePath", "Please select an image.")

        image_specifications.add_instructions(value="Select an image by clicking on the\n"
                                                    "\"Search image\" button and then click\n"
                                                    "apply. Left click on the drawing pad\n"
                                                    "to select the first point and then left\n"
                                                    "click again to place the image.\n"
                                                    "\n"
                                                    "Hold down shift while placing the\n"
                                                    "image to fix the aspect ratio of the\n"
                                                    "image.")

        set_item_callback("Apply", callback=apply_settings_dispatcher, callback_data="image tool")
        set_item_callback("Cancel", callback=apply_settings_dispatcher, callback_data="cancel tool")


# Setting up a new thread for running the tool scripts
def tool_callback_dispatcher(sender):
    tool_thread = threading.Thread(name="toolCallbackThread", target=tool_callbacks, args=(sender,), daemon=True)
    tool_thread.start()


def theme_switcher(sender):
    if sender == "dark mode":
        delete_item("dark mode")
        add_image_button(name="light mode", value="icons/light-mode.png", width=45, height=45, frame_padding=5,
                         tip="Switch to light mode", parent="miscTools", callback=theme_switcher)

        set_theme_item(mvGuiCol_Text, 255, 255, 255, 255)
        set_theme_item(mvGuiCol_PopupBg, 40, 40, 40, 255)
        set_theme_item(mvGuiCol_Border, 160, 160, 160, 70)

        set_item_color("Main Window", color=[55, 55, 55], style=mvGuiCol_WindowBg)
        set_item_color("Main Window", color=[55, 55, 55], style=mvGuiCol_MenuBarBg)

        set_item_color("Tools", color=[40, 40, 40], style=mvGuiCol_WindowBg)
        set_item_color("Tools", color=[50, 50, 50], style=mvGuiCol_TitleBg)
        set_item_color("Tools", color=[50, 50, 50], style=mvGuiCol_TitleBgActive)
        set_item_color("Tools", color=[65, 65, 65], style=mvGuiCol_Button)
        set_item_color("Tools", color=[40, 40, 40], style=mvGuiCol_ButtonHovered)
        set_item_color("Tools", color=[40, 40, 40], style=mvGuiCol_ButtonActive)
        set_item_color("Tools", color=[40, 40, 40], style=mvGuiCol_ScrollbarBg)
        set_item_color("Tools", color=[100, 100, 100], style=mvGuiCol_ScrollbarGrab)

        set_item_color("miscTools", color=[40, 40, 40], style=mvGuiCol_WindowBg)
        set_item_color("miscTools", color=[50, 50, 50], style=mvGuiCol_TitleBg)
        set_item_color("miscTools", color=[50, 50, 50], style=mvGuiCol_TitleBgActive)
        set_item_color("miscTools", color=[65, 65, 65], style=mvGuiCol_Button)
        set_item_color("miscTools", color=[40, 40, 40], style=mvGuiCol_ButtonHovered)
        set_item_color("miscTools", color=[40, 40, 40], style=mvGuiCol_ButtonActive)
        set_item_color("miscTools", color=[40, 40, 40], style=mvGuiCol_ScrollbarBg)
        set_item_color("miscTools", color=[100, 100, 100], style=mvGuiCol_ScrollbarGrab)

        set_item_color("reset", color=[55, 55, 55], style=mvGuiCol_WindowBg)
        set_item_color("reset", color=[50, 50, 50], style=mvGuiCol_TitleBg)
        set_item_color("reset", color=[50, 50, 50], style=mvGuiCol_TitleBgActive)
        set_item_color("reset", color=[55, 55, 55], style=mvGuiCol_Button)
        set_item_color("reset", color=[40, 40, 40], style=mvGuiCol_ButtonHovered)
        set_item_color("reset", color=[40, 40, 40], style=mvGuiCol_ButtonActive)
        set_item_color("reset", color=[40, 40, 40], style=mvGuiCol_ScrollbarBg)
        set_item_color("reset", color=[100, 100, 100], style=mvGuiCol_ScrollbarGrab)

        set_item_color("SimpleDrawing Name", color=[55, 55, 55], style=mvGuiCol_WindowBg)
        set_item_color("SimpleDrawing Name", color=[160, 160, 160], style=mvGuiCol_Text)
        set_item_color("SimpleDrawing Name", color=[55, 55, 55], style=mvGuiCol_Button)
        set_item_color("SimpleDrawing Name", color=[40, 40, 40], style=mvGuiCol_ButtonHovered)
        set_item_color("SimpleDrawing Name", color=[40, 40, 40], style=mvGuiCol_ButtonActive)

        set_item_color("DPG", color=[55, 55, 55], style=mvGuiCol_WindowBg)
        set_item_color("DPG", color=[160, 160, 160], style=mvGuiCol_Text)
        set_item_color("DPG", color=[55, 55, 55], style=mvGuiCol_Button)
        set_item_color("DPG", color=[40, 40, 40], style=mvGuiCol_ButtonHovered)
        set_item_color("DPG", color=[40, 40, 40], style=mvGuiCol_ButtonActive)

        set_item_color("Mouse Pad Coordinates", color=[55, 55, 55], style=mvGuiCol_WindowBg)
        set_item_color("Mouse Pad Coordinates", color=[160, 160, 160], style=mvGuiCol_Text)

        set_item_color("Tool Specifications", color=[70, 70, 70], style=mvGuiCol_WindowBg)
        set_item_color("Tool Specifications", color=[70, 70, 70], style=mvGuiCol_TitleBg)
        set_item_color("Tool Specifications", color=[70, 70, 70], style=mvGuiCol_TitleBgActive)
        set_item_color("Tool Specifications", color=[80, 80, 80], style=mvGuiCol_Button)
        set_item_color("Tool Specifications", color=[40, 40, 40], style=mvGuiCol_ButtonHovered)
        set_item_color("Tool Specifications", color=[40, 40, 40], style=mvGuiCol_ButtonActive)
        set_item_color("Tool Specifications", color=[60, 60, 60], style=mvGuiCol_FrameBg)
        set_item_color("Tool Specifications", color=[40, 40, 40], style=mvGuiCol_FrameBgHovered)
        set_item_color("Tool Specifications", color=[40, 40, 40], style=mvGuiCol_FrameBgActive)
        set_item_color("Tool Specifications", color=[80, 80, 80], style=mvGuiCol_ChildBg)

        set_item_color("Drawing Pad", color=[95, 95, 95], style=mvGuiCol_TitleBg)
        set_item_color("Drawing Pad", color=[95, 95, 95], style=mvGuiCol_TitleBgActive)

        delete_item("Tools", children_only=True)

        add_image_button(name="straight line tool", value="icons/dark-straight-line-tool.png", width=45, height=45,
                         frame_padding=5, tip="Straight line tool", callback=tool_callback_dispatcher, parent="Tools")
        add_spacing(count=1)
        add_image_button(name="dashed line tool", value="icons/dark-dashed-line-tool.png", width=45, height=45,
                         frame_padding=5,
                         tip="Dashed line tool", callback=tool_callback_dispatcher, parent="Tools")
        add_spacing(count=1, parent="Tools")
        add_image_button(name="polyline tool", value="icons/dark-polyline-tool.png", width=45, height=45, frame_padding=5,
                         tip="Polyline tool", callback=tool_callback_dispatcher, parent="Tools")
        add_spacing(count=1, parent="Tools")
        add_image_button(name="doodle tool", value="icons/dark-doodle-tool.png", width=45, height=45, frame_padding=5,
                         tip="Doodle tool", callback=tool_callback_dispatcher, parent="Tools")
        add_spacing(count=1, parent="Tools")
        add_image_button(name="rectangle tool", value="icons/dark-rectangle-tool.png", width=45, height=45, frame_padding=5,
                         tip="Rectangle tool", callback=tool_callback_dispatcher, parent="Tools")
        add_spacing(count=1, parent="Tools")
        add_image_button(name="circle tool", value="icons/dark-circle-tool.png", width=45, height=45, frame_padding=5,
                         tip="Circle tool", callback=tool_callback_dispatcher, parent="Tools")
        add_spacing(count=1, parent="Tools")
        add_image_button(name="arrow tool", value="icons/dark-arrow-tool.png", width=45, height=45, frame_padding=5,
                         tip="Arrow tool", callback=tool_callback_dispatcher, parent="Tools")
        add_spacing(count=1, parent="Tools")
        add_image_button(name="bezier tool", value="icons/dark-bezier-tool.png", width=45, height=45, frame_padding=5,
                         tip="Bezier tool", callback=tool_callback_dispatcher, parent="Tools")
        add_spacing(count=1, parent="Tools")
        add_image_button(name="text tool", value="icons/dark-text-tool.png", width=45, height=45, frame_padding=5,
                         tip="Text tool", callback=tool_callback_dispatcher, parent="Tools")
        add_spacing(count=1, parent="Tools")
        add_image_button(name="image tool", value="icons/dark-image-tool.png", width=45, height=45, frame_padding=5,
                         tip="Image tool", callback=tool_callback_dispatcher, parent="Tools")

        delete_item("reset", children_only=True)

        add_image_button(name="reset tool", value="icons/dark-reset-tool.png", width=45, height=45, frame_padding=5,
                         tip="Reset entire drawing pad", parent="reset")

        with popup(popupparent="reset tool", name="Are you sure you want to erase the drawing pad?", modal=True,
                   mousebutton=mvMouseButton_Left):
            add_spacing(count=1)
            add_button("Yes##reset", width=150, height=25, callback=tool_callback_dispatcher)
            add_same_line(spacing=10)
            add_button("No##reset", width=150, height=25, callback=tool_callback_dispatcher)

            set_item_style_var("Are you sure you want to erase the drawing pad?", style=mvGuiStyleVar_FrameBorderSize,
                               value=[1])
            set_item_style_var("Are you sure you want to erase the drawing pad?", style=mvGuiStyleVar_WindowRounding,
                               value=[12])

    if sender == "light mode":
        delete_item("light mode")
        add_image_button(name="dark mode", value="icons/dark-mode.png", width=45, height=45, frame_padding=5,
                         tip="Switch to dark mode", parent="miscTools", callback=theme_switcher)

        set_theme_item(mvGuiCol_Text, 0, 0, 0, 255)
        set_theme_item(mvGuiCol_PopupBg, 255, 255, 255, 255)
        set_theme_item(mvGuiCol_Border, 100, 100, 100, 70)

        set_item_color("Main Window", color=[225, 225, 225], style=mvGuiCol_WindowBg)
        set_item_color("Main Window", color=[225, 225, 225], style=mvGuiCol_MenuBarBg)

        set_item_color("Tools", color=[200, 200, 200], style=mvGuiCol_WindowBg)
        set_item_color("Tools", color=[225, 225, 225], style=mvGuiCol_TitleBg)
        set_item_color("Tools", color=[225, 225, 225], style=mvGuiCol_TitleBgActive)
        set_item_color("Tools", color=[225, 225, 225], style=mvGuiCol_Button)
        set_item_color("Tools", color=[200, 200, 200], style=mvGuiCol_ButtonHovered)
        set_item_color("Tools", color=[200, 200, 200], style=mvGuiCol_ButtonActive)
        set_item_color("Tools", color=[200, 200, 200], style=mvGuiCol_ScrollbarBg)
        set_item_color("Tools", color=[160, 160, 160], style=mvGuiCol_ScrollbarGrab)

        set_item_color("miscTools", color=[200, 200, 200], style=mvGuiCol_WindowBg)
        set_item_color("miscTools", color=[225, 225, 225], style=mvGuiCol_TitleBg)
        set_item_color("miscTools", color=[225, 225, 225], style=mvGuiCol_TitleBgActive)
        set_item_color("miscTools", color=[225, 225, 225], style=mvGuiCol_Button)
        set_item_color("miscTools", color=[200, 200, 200], style=mvGuiCol_ButtonHovered)
        set_item_color("miscTools", color=[200, 200, 200], style=mvGuiCol_ButtonActive)
        set_item_color("miscTools", color=[200, 200, 200], style=mvGuiCol_ScrollbarBg)
        set_item_color("miscTools", color=[160, 160, 160], style=mvGuiCol_ScrollbarGrab)

        set_item_color("reset", color=[225, 225, 225], style=mvGuiCol_WindowBg)
        set_item_color("reset", color=[225, 225, 225], style=mvGuiCol_TitleBg)
        set_item_color("reset", color=[225, 225, 225], style=mvGuiCol_TitleBgActive)
        set_item_color("reset", color=[225, 225, 225], style=mvGuiCol_Button)
        set_item_color("reset", color=[200, 200, 200], style=mvGuiCol_ButtonHovered)
        set_item_color("reset", color=[200, 200, 200], style=mvGuiCol_ButtonActive)
        set_item_color("reset", color=[200, 200, 200], style=mvGuiCol_ScrollbarBg)
        set_item_color("reset", color=[160, 160, 160], style=mvGuiCol_ScrollbarGrab)

        set_item_color("SimpleDrawing Name", color=[225, 225, 225], style=mvGuiCol_WindowBg)
        set_item_color("SimpleDrawing Name", color=[100, 100, 100], style=mvGuiCol_Text)
        set_item_color("SimpleDrawing Name", color=[225, 225, 225], style=mvGuiCol_Button)
        set_item_color("SimpleDrawing Name", color=[200, 200, 200], style=mvGuiCol_ButtonHovered)
        set_item_color("SimpleDrawing Name", color=[200, 200, 200], style=mvGuiCol_ButtonActive)

        set_item_color("DPG", color=[225, 225, 225], style=mvGuiCol_WindowBg)
        set_item_color("DPG", color=[100, 100, 100], style=mvGuiCol_Text)
        set_item_color("DPG", color=[225, 225, 225], style=mvGuiCol_Button)
        set_item_color("DPG", color=[200, 200, 200], style=mvGuiCol_ButtonHovered)
        set_item_color("DPG", color=[200, 200, 200], style=mvGuiCol_ButtonActive)

        set_item_color("Mouse Pad Coordinates", color=[225, 225, 225], style=mvGuiCol_WindowBg)
        set_item_color("Mouse Pad Coordinates", color=[100, 100, 100], style=mvGuiCol_Text)

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

        set_item_color("Drawing Pad", color=[255, 255, 255], style=mvGuiCol_TitleBg)
        set_item_color("Drawing Pad", color=[255, 255, 255], style=mvGuiCol_TitleBgActive)

        delete_item("Tools", children_only=True)

        add_image_button(name="straight line tool", value="icons/straight-line-tool.png", width=45, height=45,
                         frame_padding=5, tip="Straight line tool", callback=tool_callback_dispatcher, parent="Tools")
        add_spacing(count=1)
        add_image_button(name="dashed line tool", value="icons/dashed-line-tool.png", width=45, height=45,
                         frame_padding=5,
                         tip="Dashed line tool", callback=tool_callback_dispatcher, parent="Tools")
        add_spacing(count=1, parent="Tools")
        add_image_button(name="polyline tool", value="icons/polyline-tool.png", width=45, height=45, frame_padding=5,
                         tip="Polyline tool", callback=tool_callback_dispatcher, parent="Tools")
        add_spacing(count=1, parent="Tools")
        add_image_button(name="doodle tool", value="icons/doodle-tool.png", width=45, height=45, frame_padding=5,
                         tip="Doodle tool", callback=tool_callback_dispatcher, parent="Tools")
        add_spacing(count=1, parent="Tools")
        add_image_button(name="rectangle tool", value="icons/rectangle-tool.png", width=45, height=45, frame_padding=5,
                         tip="Rectangle tool", callback=tool_callback_dispatcher, parent="Tools")
        add_spacing(count=1, parent="Tools")
        add_image_button(name="circle tool", value="icons/circle-tool.png", width=45, height=45, frame_padding=5,
                         tip="Circle tool", callback=tool_callback_dispatcher, parent="Tools")
        add_spacing(count=1, parent="Tools")
        add_image_button(name="arrow tool", value="icons/arrow-tool.png", width=45, height=45, frame_padding=5,
                         tip="Arrow tool", callback=tool_callback_dispatcher, parent="Tools")
        add_spacing(count=1, parent="Tools")
        add_image_button(name="bezier tool", value="icons/bezier-tool.png", width=45, height=45, frame_padding=5,
                         tip="Bezier tool", callback=tool_callback_dispatcher, parent="Tools")
        add_spacing(count=1, parent="Tools")
        add_image_button(name="text tool", value="icons/text-tool.png", width=45, height=45, frame_padding=5,
                         tip="Text tool", callback=tool_callback_dispatcher, parent="Tools")
        add_spacing(count=1, parent="Tools")
        add_image_button(name="image tool", value="icons/image-tool.png", width=45, height=45, frame_padding=5,
                         tip="Image tool", callback=tool_callback_dispatcher, parent="Tools")

        delete_item("reset", children_only=True)

        add_image_button(name="reset tool", value="icons/reset-tool.png", width=45, height=45, frame_padding=5,
                         tip="Reset entire drawing pad", parent="reset")

        with popup(popupparent="reset tool", name="Are you sure you want to erase the drawing pad?", modal=True,
                   mousebutton=mvMouseButton_Left):
            add_spacing(count=1)
            add_button("Yes##reset", width=150, height=25, callback=tool_callback_dispatcher)
            add_same_line(spacing=10)
            add_button("No##reset", width=150, height=25, callback=tool_callback_dispatcher)
            set_item_style_var("Are you sure you want to erase the drawing pad?", style=mvGuiStyleVar_WindowRounding,
                               value=[12])

# Main Window widget
with window("Main Window"):
    # Main Window styling
    set_main_window_title("SimpleDrawing")
    set_main_window_pos(x=0, y=0)
    set_main_window_size(width=1370, height=740)
    set_main_window_resizable(False)
    add_additional_font("fonts/OpenSans-Regular.ttf", 18)

    set_style_item_spacing(20.00, 5.00)
    set_style_item_inner_spacing(0.00, 0.00)
    set_style_touch_extra_padding(0.00, 0.00)
    set_style_window_border_size(0.00)
    set_style_window_rounding(0.00)
    set_style_window_title_align(0.50, 0.50)
    set_style_window_padding(20, 5)
    set_style_frame_border_size(1.0)

    # Main Window colors
    set_theme("Light")
    set_theme_item(mvGuiCol_Border, 100, 100, 100, 70)
    set_item_color("Main Window", color=[225, 225, 225], style=mvGuiCol_WindowBg)

    with menu_bar("Main menu bar"):
        with menu("File"):
            add_menu_item("Open drawing", callback=tools.openTool, shortcut='Ctrl + O')
            add_menu_item("Save drawing", callback=tools.saveTool, shortcut='Ctrl + S')
            add_menu_item("Exit", callback=lambda: stop_dearpygui())

        with menu("Edit"):
            add_menu_item("Undo", callback=lambda data: read_db(action="undo"), shortcut='Ctrl + Z')
            add_menu_item("Redo", callback=lambda data: read_db(action="redo"), shortcut='Ctrl + Y')

        with menu("Tools##menu"):
            add_menu_item("Straight line tool", callback=lambda data: tool_callback_dispatcher(sender="straight line tool"))
            add_menu_item("Dashed line tool", callback=lambda data: tool_callback_dispatcher(sender="dashed line tool"))
            add_menu_item("Polyline tool", callback=lambda data: tool_callback_dispatcher(sender="polyline tool"))
            add_menu_item("Doodle tool", callback=lambda data: tool_callback_dispatcher(sender="doodle tool"))
            add_menu_item("Rectangle tool", callback=lambda data: tool_callback_dispatcher(sender="rectangle tool"))
            add_menu_item("Circle tool", callback=lambda data: tool_callback_dispatcher(sender="circle tool"))
            add_menu_item("Arrow tool", callback=lambda data: tool_callback_dispatcher(sender="arrow tool"))
            add_menu_item("Bezier tool", callback=lambda data: tool_callback_dispatcher(sender="bezier tool"))
            add_menu_item("Text tool", callback=lambda data: tool_callback_dispatcher(sender="text tool"))
            add_menu_item("Image tool", callback=lambda data: tool_callback_dispatcher(sender="image tool"))

        with menu("Help"):
            add_menu_item("About", callback=open_website, callback_data="https://github.com/RahulShagri/SimpleDrawing-Desktop-App")

# Tools window widget
with window("Tools", no_collapse=True, no_resize=True, no_move=True, no_close=True, x_pos=0, y_pos=25, width=80,
            height=425):
    # Tool Bar window styling
    set_item_color("Tools", color=[200, 200, 200], style=mvGuiCol_WindowBg)
    set_item_color("Tools", color=[225, 225, 225], style=mvGuiCol_TitleBg)
    set_item_color("Tools", color=[225, 225, 225], style=mvGuiCol_TitleBgActive)
    set_item_color("Tools", color=[225, 225, 225], style=mvGuiCol_Button)
    set_item_color("Tools", color=[200, 200, 200], style=mvGuiCol_ButtonHovered)
    set_item_color("Tools", color=[200, 200, 200], style=mvGuiCol_ButtonActive)
    set_item_color("Tools", color=[200, 200, 200], style=mvGuiCol_ScrollbarBg)
    set_item_color("Tools", color=[160, 160, 160], style=mvGuiCol_ScrollbarGrab)

    set_item_style_var("Tools", style=mvGuiStyleVar_FrameRounding, value=[12])
    set_item_style_var("Tools", style=mvGuiStyleVar_ScrollbarSize,value=[10])
    set_item_style_var("Tools", style=mvGuiStyleVar_WindowBorderSize, value=[1])
    set_item_style_var("Tools", style=mvGuiStyleVar_WindowPadding, value=[8, 8])

    # General sketching tool buttons
    add_image_button(name="straight line tool", value="icons/straight-line-tool.png", width=45, height=45,
                     frame_padding=5, tip="Straight line tool", callback=tool_callback_dispatcher)
    add_spacing(count=1)
    add_image_button(name="dashed line tool", value="icons/dashed-line-tool.png", width=45, height=45, frame_padding=5,
                     tip="Dashed line tool", callback=tool_callback_dispatcher)
    add_spacing(count=1)
    add_image_button(name="polyline tool", value="icons/polyline-tool.png", width=45, height=45, frame_padding=5,
                     tip="Polyline tool", callback=tool_callback_dispatcher)
    add_spacing(count=1)
    add_image_button(name="doodle tool", value="icons/doodle-tool.png", width=45, height=45, frame_padding=5,
                     tip="Doodle tool", callback=tool_callback_dispatcher)
    add_spacing(count=1)
    add_image_button(name="rectangle tool", value="icons/rectangle-tool.png", width=45, height=45, frame_padding=5,
                     tip="Rectangle tool", callback=tool_callback_dispatcher)
    add_spacing(count=1)
    add_image_button(name="circle tool", value="icons/circle-tool.png", width=45, height=45, frame_padding=5,
                     tip="Circle tool", callback=tool_callback_dispatcher)
    add_spacing(count=1)
    add_image_button(name="arrow tool", value="icons/arrow-tool.png", width=45, height=45, frame_padding=5,
                     tip="Arrow tool", callback=tool_callback_dispatcher)
    add_spacing(count=1)
    add_image_button(name="bezier tool", value="icons/bezier-tool.png", width=45, height=45, frame_padding=5,
                     tip="Bezier tool", callback=tool_callback_dispatcher)
    add_spacing(count=1)
    add_image_button(name="text tool", value="icons/text-tool.png", width=45, height=45, frame_padding=5,
                     tip="Text tool", callback=tool_callback_dispatcher)
    add_spacing(count=1)
    add_image_button(name="image tool", value="icons/image-tool.png", width=45, height=45, frame_padding=5,
                     tip="Image tool", callback=tool_callback_dispatcher)

with window("miscTools", no_collapse=True, no_resize=True, no_move=True, no_close=True, x_pos=5, y_pos=460, width=70,
            height=140, no_title_bar=True):
    set_item_color("miscTools", color=[200, 200, 200], style=mvGuiCol_WindowBg)
    set_item_color("miscTools", color=[225, 225, 225], style=mvGuiCol_TitleBg)
    set_item_color("miscTools", color=[225, 225, 225], style=mvGuiCol_TitleBgActive)
    set_item_color("miscTools", color=[225, 225, 225], style=mvGuiCol_Button)
    set_item_color("miscTools", color=[200, 200, 200], style=mvGuiCol_ButtonHovered)
    set_item_color("miscTools", color=[200, 200, 200], style=mvGuiCol_ButtonActive)
    set_item_color("miscTools", color=[200, 200, 200], style=mvGuiCol_ScrollbarBg)
    set_item_color("miscTools", color=[160, 160, 160], style=mvGuiCol_ScrollbarGrab)

    set_item_style_var("miscTools", style=mvGuiStyleVar_FrameRounding, value=[12])
    set_item_style_var("miscTools", style=mvGuiStyleVar_ScrollbarSize,value=[10])
    set_item_style_var("miscTools", style=mvGuiStyleVar_WindowBorderSize, value=[1])
    set_item_style_var("miscTools", style=mvGuiStyleVar_WindowPadding, value=[8, 8])

    add_image_button(name="canvas color tool", value="icons/canvas-color-tool.png", width=45, height=45, frame_padding=5,
                     tip="Change canvas color", callback=tool_callback_dispatcher)
    add_spacing(count=1)
    add_image_button(name="dark mode", value="icons/dark-mode.png", width=45, height=45, frame_padding=5,
                     tip="Switch to dark mode", callback=theme_switcher)

with window("reset", no_collapse=True, no_resize=True, no_move=True, no_close=True, x_pos=5, y_pos=600, width=70,
            height=73, no_title_bar=True):
    set_item_color("reset", color=[225, 225, 225], style=mvGuiCol_WindowBg)
    set_item_color("reset", color=[225, 225, 225], style=mvGuiCol_TitleBg)
    set_item_color("reset", color=[225, 225, 225], style=mvGuiCol_TitleBgActive)
    set_item_color("reset", color=[225, 225, 225], style=mvGuiCol_Button)
    set_item_color("reset", color=[200, 200, 200], style=mvGuiCol_ButtonHovered)
    set_item_color("reset", color=[200, 200, 200], style=mvGuiCol_ButtonActive)
    set_item_color("reset", color=[200, 200, 200], style=mvGuiCol_ScrollbarBg)
    set_item_color("reset", color=[160, 160, 160], style=mvGuiCol_ScrollbarGrab)

    set_item_style_var("reset", style=mvGuiStyleVar_FrameRounding, value=[12])
    set_item_style_var("reset", style=mvGuiStyleVar_ScrollbarSize,value=[10])
    set_item_style_var("reset", style=mvGuiStyleVar_WindowBorderSize, value=[0])
    set_item_style_var("reset", style=mvGuiStyleVar_FrameBorderSize, value=[0])
    set_item_style_var("reset", style=mvGuiStyleVar_WindowPadding, value=[8, 8])

    add_image_button(name="reset tool", value="icons/reset-tool.png", width=45, height=45, frame_padding=5,
                     tip="Reset entire drawing pad")


    with popup(popupparent="reset tool", name="Are you sure you want to erase the drawing pad?", modal=True, mousebutton=mvMouseButton_Left):
        add_spacing(count=1)
        add_button("Yes##reset", width=150, height=25, callback=tool_callback_dispatcher)
        add_same_line(spacing=10)
        add_button("No##reset", width=150, height=25, callback=tool_callback_dispatcher)

        set_item_style_var("Are you sure you want to erase the drawing pad?", style=mvGuiStyleVar_FrameBorderSize, value=[1])
        set_item_style_var("Are you sure you want to erase the drawing pad?", style=mvGuiStyleVar_WindowRounding,
                           value=[12])

# Tool Specifications window widget
with window("Tool Specifications", no_collapse=True, no_resize=True, no_move=True, no_close=True, x_pos=80, y_pos=25,
            width=245, height=644):
    # Tool Specifications window styling
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
    set_item_style_var("Tool Specifications", style=mvGuiStyleVar_WindowPadding, value=[8, 8])

    add_text("To get started, please select one of\nthe tools from the column on the\nleft.")

# ----Drawing Pad window widget----#
with window("Drawing Pad", no_close=True, no_collapse=True, no_resize=True, x_pos=325, y_pos=25, autosize=True,
            no_move=True):
    # Drawing Pad window styling
    set_item_color("Drawing Pad", color=[255, 255, 255], style=mvGuiCol_WindowBg)
    set_item_color("Drawing Pad", color=[255, 255, 255], style=mvGuiCol_TitleBg)
    set_item_color("Drawing Pad", color=[255, 255, 255], style=mvGuiCol_TitleBgActive)

    set_item_style_var("Drawing Pad", style=mvGuiStyleVar_WindowPadding, value=[8, 8])

    # Adding drawing canvas
    add_drawing("Pad", height=604, width=1025)

# Window to display mouse coordinates
with window("Mouse Pad Coordinates", no_close=True, no_collapse=True, no_resize=True, no_title_bar=True, x_pos=1130,
            y_pos=670, no_move=True, height=50, width=250):
    set_item_color("Mouse Pad Coordinates", color=[225, 225, 225], style=mvGuiCol_WindowBg)
    set_item_color("Mouse Pad Coordinates", color=[100, 100, 100], style=mvGuiCol_Text)

    set_item_style_var("Mouse Pad Coordinates", style=mvGuiStyleVar_WindowPadding, value=[8, 8])

    add_text("Mouse coordinates:")

# Window to display SimpleDrawing version number
with window("SimpleDrawing Name", no_close=True, no_collapse=True, no_resize=True, no_title_bar=True, x_pos=80,
            y_pos=678, no_move=True, height=50, width=100):

    set_item_color("SimpleDrawing Name", color=[225, 225, 225], style=mvGuiCol_WindowBg)
    set_item_color("SimpleDrawing Name", color=[100, 100, 100], style=mvGuiCol_Text)
    set_item_color("SimpleDrawing Name", color=[225, 225, 225], style=mvGuiCol_Button)
    set_item_color("SimpleDrawing Name", color=[200, 200, 200], style=mvGuiCol_ButtonHovered)
    set_item_color("SimpleDrawing Name", color=[200, 200, 200], style=mvGuiCol_ButtonActive)

    set_item_style_var("SimpleDrawing Name", style=mvGuiStyleVar_FrameBorderSize, value=[0])
    set_item_style_var("SimpleDrawing Name", style=mvGuiStyleVar_WindowPadding, value=[0, 0])
    set_item_style_var("SimpleDrawing Name", style=mvGuiStyleVar_FramePadding, value=[0, 0])

    add_button("SimpleDrawing", callback=open_website, callback_data="https://github.com/RahulShagri/SimpleDrawing-Desktop-App")

# Window to credit Dear PyGui
with window("DPG", no_close=True, no_collapse=True, no_resize=True, no_title_bar=True, x_pos=325, y_pos=678,
            no_move=True, height=25, width=155):

    set_item_color("DPG", color=[225, 225, 225], style=mvGuiCol_WindowBg)
    set_item_color("DPG", color=[100, 100, 100], style=mvGuiCol_Text)
    set_item_color("DPG", color=[225, 225, 225], style=mvGuiCol_Button)
    set_item_color("DPG", color=[200, 200, 200], style=mvGuiCol_ButtonHovered)
    set_item_color("DPG", color=[200, 200, 200], style=mvGuiCol_ButtonActive)

    set_item_style_var("DPG", style=mvGuiStyleVar_FrameBorderSize, value=[0])
    set_item_style_var("DPG", style=mvGuiStyleVar_WindowPadding, value=[0, 0])
    set_item_style_var("DPG", style=mvGuiStyleVar_FramePadding, value=[0, 0])

    add_button("Powered by Dear PyGui", callback=open_website, callback_data="https://github.com/hoffstadt/DearPyGui")

set_mouse_move_callback(pad_mouse_coordinates)
set_key_down_callback(tools.hotkeyCommands)

def main():
    create_db()
    # Start app
    start_dearpygui(primary_window="Main Window")

if __name__ == '__main__':
    main()
