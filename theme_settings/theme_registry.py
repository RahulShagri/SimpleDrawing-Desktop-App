# Add themes
import dearpygui.dearpygui as dpg

with dpg.theme(default_theme=True):
    # Styles
    dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, 4, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 4, 4, category=dpg.mvThemeCat_Core)

    # Colors
    dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (33, 33, 33), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (48, 48, 48), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_Text, (200, 200, 200), category=dpg.mvThemeCat_Core)

with dpg.theme() as menu_bar_theme:
    # Styles
    dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 15, 12, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 20, 10, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 8, 4, category=dpg.mvThemeCat_Core)
    # Colors

with dpg.theme() as tool_bar_theme:
    # Styles
    dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 10, 4, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 12, category=dpg.mvThemeCat_Core)

    # Colors
    dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (33, 33, 33), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_Button, (33, 33, 33), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (48, 48, 48), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (79, 117, 179), category=dpg.mvThemeCat_Core)

with dpg.theme() as tool_active_theme:
    # Colors
    dpg.add_theme_color(dpg.mvThemeCol_Button, (79, 117, 179), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (79, 117, 179), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (79, 117, 179), category=dpg.mvThemeCat_Core)

with dpg.theme() as drawing_pad_theme:
    # Styles
    dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 6, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0, category=dpg.mvThemeCat_Core)

    # Colors
    dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (255, 255, 255), category=dpg.mvThemeCat_Core)

with dpg.theme() as tool_properties_theme:
    # Styles
    dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 1, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 6, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 8, 8, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 8, 2, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 12, category=dpg.mvThemeCat_Core)

    # Colors
    dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (56, 56, 56), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (200, 200, 200), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (89, 89, 89), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (128, 128, 128), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (96, 96, 96), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg, (56, 56, 56), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (56, 56, 56), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (56, 56, 56), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_Border, (56, 56, 56), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_Button, (89, 89, 89), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (105, 105, 105), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (79, 117, 179), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (56, 56, 56), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (104, 104, 104), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, (104, 104, 104), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, (108, 108, 108), category=dpg.mvThemeCat_Core)

with dpg.theme() as layer_properties_theme:
    # Styles
    dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 1, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 6, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 8, 10, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 4, 4, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 8, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 12, category=dpg.mvThemeCat_Core)

    # Colors
    dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (66, 66, 66), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_Border, (66, 66, 66), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_Separator, (90, 90, 90), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (104, 104, 104), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, (104, 104, 104), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, (108, 108, 108), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (53, 53, 53), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (105, 105, 105), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (200, 200, 200), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (200, 200, 200), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_Button, (66, 66, 66), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (105, 105, 105), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (79, 117, 179), category=dpg.mvThemeCat_Core)

with dpg.theme() as info_bar_theme:
    # Styles
    dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 1, 1, category=dpg.mvThemeCat_Core)

    # Colors
    dpg.add_theme_color(dpg.mvThemeCol_Text, (180, 180, 180), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (48, 48, 48), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_Button, (48, 48, 48), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (33, 33, 33), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (33, 33, 33), category=dpg.mvThemeCat_Core)

with dpg.theme() as welcome_window_theme:
    # Styles
    dpg.add_theme_style(dpg.mvStyleVar_WindowTitleAlign, 0.5, 1, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 12, 12, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 6, 6, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 8, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0, category=dpg.mvThemeCat_Core)

    # Colors
    dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (34, 34, 34), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (34, 34, 34), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_Button, (34, 34, 34), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (79, 117, 179), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (79, 117, 179), category=dpg.mvThemeCat_Core)

with dpg.theme() as popup_theme:
    # Styles
    dpg.add_theme_style(dpg.mvStyleVar_WindowTitleAlign, 0.5, 1, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 12, 15, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 6, 6, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 8, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 8, category=dpg.mvThemeCat_Core)

    # Colors
    dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (34, 34, 34, 220), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (78, 78, 78), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (34, 34, 34, 220), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_Button, (88, 88, 88), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (106, 106, 106), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (79, 117, 179), category=dpg.mvThemeCat_Core)

with dpg.theme() as combo_theme:
    # Styles
    dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 15, 6, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 4, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, 6, category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, 12, category=dpg.mvThemeCat_Core)

    # Colors
    dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (44, 44, 44), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (53, 53, 53), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (44, 44, 44), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_Button, (44, 44, 44), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (53, 53, 53), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (105, 109, 118), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (79, 117, 179), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (79, 117, 179), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (33, 33, 33, 220), category=dpg.mvThemeCat_Core)

with dpg.theme() as tool_properties_group_theme:
    # Styles
    dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 4, 15, category=dpg.mvThemeCat_Core)

with dpg.theme() as layer_list_theme:
    # Styles

    # Colors
    dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (53, 53, 53), category=dpg.mvThemeCat_Core)
