from dearpygui.core import *
from dearpygui.simple import *
from time import sleep
import multiprocessing

def what_window():
    pass
    #print(get_active_window())

def draw_start(str):
    '''count = 20

    for i in range(10):
        draw_line("New draw", p1=[count, 40], p2=[count, 100], thickness=5, color=[255, 255, 255])
        sleep(3)
        count += 20'''

    now_time = 0
    while True:
        if is_mouse_button_released(mvMouseButton_Right):
            print('right down')
        else:
            continue

def long_dispatcher():
    #d = threading.Thread(name="daemon", target=draw_start("test this"), daemon=True)
    d = multiprocessing.Process(target=draw_start, args=('new', ))
    d.start()

    sleep(5)

    d.terminate()

with window("This", x_pos=0):
    add_text("This is text")
    add_button("start", callback=long_dispatcher)

with window("Drawing", autosize=True, x_pos=400):
    add_drawing("New draw", height=400, width=400)

set_mouse_down_callback(what_window)

start_dearpygui()
