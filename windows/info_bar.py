import dearpygui.dearpygui as dpg
from windows.base_window import *
import webbrowser

screen_width, screen_height = get_screen_resolution()


def open_docs(sender, app_data, user_data):
    webbrowser.open(user_data)


dpg.add_button(label='SimpleDrawing', parent=info_bar, pos=[15, 2], callback=open_docs,
               user_data='https://github.com/RahulShagri/SimpleDrawing-Desktop-App')

dpg.add_button(label='Powered by Dear PyGui', parent=info_bar, pos=[int(screen_width/2) - 60, 2],
               callback=open_docs, user_data='https://github.com/hoffstadt/DearPyGui')

dpg.add_button(label='v1.0.0', parent=info_bar, pos=[int(screen_width) - 50, 2],
               callback=open_docs, user_data='https://github.com/RahulShagri/SimpleDrawing-Desktop-App')
