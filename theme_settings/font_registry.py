# Add all fonts
import dearpygui.dearpygui as dpg

with dpg.font_registry() as main_font_registry:
    regular_font = dpg.add_font('fonts/Roboto/Roboto-Regular.ttf', 16, default_font=True)
    bold_font = dpg.add_font('fonts/Roboto/Roboto-Bold.ttf', 20)
    italic_font = dpg.add_font('fonts/Roboto/Roboto-Italic.ttf', 16)
    small_font = dpg.add_font('fonts/Roboto/Roboto-Light.ttf', 15)
