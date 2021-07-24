# Import Dear PyGui
import dearpygui.dearpygui as dpg

# Import package with all windows (Automatically configures main viewport and sets up the base layout on call)
import windows
import managers

# Record screen resolution
screen_width, screen_height = windows.get_screen_resolution()

# Subtract Taskbar and title bar height
screen_height = screen_height - int(0.05*screen_height)

# Show welcome window
# windows.run_welcome_window(screen_width, screen_height)

# Initiate Dear PyGui
dpg.start_dearpygui()
