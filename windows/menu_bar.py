import dearpygui.dearpygui as dpg
from windows.base_window import *

with dpg.menu(label='File', parent=menu_bar_top):
    dpg.add_menu_item(label='New project', shortcut='Ctrl + N')
    dpg.add_menu_item(label='Open project', shortcut='Ctrl + O')
    dpg.add_menu_item(label='Save Project', shortcut='Ctrl + S')
    dpg.add_menu_item(label='Save As Project', shortcut='Ctrl + Shift + S')

with dpg.menu(label='Tools', parent=menu_bar_top):
    pass

with dpg.menu(label='Help', parent=menu_bar_top):
    dpg.add_menu_item(label='Read the docs')
