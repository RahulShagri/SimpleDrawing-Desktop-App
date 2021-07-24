# Get screen resolution

def get_screen_resolution():
    import tkinter as tk

    root = tk.Tk()
    return root.winfo_screenwidth(), root.winfo_screenheight()