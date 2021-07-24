import dearpygui.dearpygui as dpg
from windows.base_window import *
from tools import *


class Tool:
    def __init__(self, tool_name: str, icon_image: str):
        self.tool_name = tool_name

        # Get image information and set a texture
        width, height, channels, data = dpg.load_image(icon_image)
        with dpg.texture_registry():
            texture_id = dpg.add_static_texture(width, height, data)

        # Create an image button using that image
        self.tool_button = dpg.add_image_button(texture_id, width=43, height=43, parent=tool_group,
                                                callback=self.useTool)

    def useTool(self):
        # Reset the tool_properties child window (will be recreated later)
        dpg.delete_item(item=tool_properties, children_only=True)

        # Reset all buttons' theme to parent (tool_bar) theme to get rid of the active_theme from the tools
        for tool_item in dpg.get_item_children(item=tool_group)[1][1:]:
            dpg.set_item_theme(item=tool_item, theme=0)

        # Set active theme to show that the tool clicked is now active
        dpg.set_item_theme(item=self.tool_button, theme=tool_active_theme)

        # Call the tool appropriate function to create a table inside the tool_properties child window
        eval(f"set_{self.tool_name}_properties()")

        # Initiate the tool by calling the dispatcher to create a new thread
        eval(f"{self.tool_name}Dispatcher()")


lineTool = Tool(tool_name="lineTool", icon_image="icons/lineTool.png")
doodleTool = Tool(tool_name="doodleTool", icon_image="icons/doodleTool.png")
rectangleTool = Tool(tool_name="rectangleTool", icon_image="icons/rectangleTool.png")
circleTool = Tool(tool_name="circleTool", icon_image="icons/circleTool.png")
ellipseTool = Tool(tool_name="ellipseTool", icon_image="icons/ellipseTool.png")
textTool = Tool(tool_name="textTool", icon_image="icons/textTool.png")
imageTool = Tool(tool_name="imageTool", icon_image="icons/imageTool.png")
imageTool.useTool()