# Import DearPyGui files
from dearpygui.core import *
from dearpygui.simple import *

class ToolSpec:
    # Class that will create all widgets inside the Tool Specifications Window
    def __init__(self, title: str, height: int):
        self.title = title
        self.height = height
        self.parent = "Tool Specifications"

        add_spacing(count=1, parent=self.parent)
        add_text(self.title, parent=self.parent)
        add_spacing(count=3, parent=self.parent)
        add_separator(parent=self.parent)
        add_spacing(count=1, parent=self.parent)

        with child("tool properties", height=self.height, parent=self.parent):
            self.add_space(count=2)

        add_button("Cancel", parent=self.parent, height=30, width=110)
        add_same_line(spacing=8.0, parent=self.parent)
        add_button("Apply", parent=self.parent, height=30, width=110)
        add_spacing(count=1, parent=self.parent)
        add_separator(parent=self.parent)

    def add_space(self, count: int):
        add_spacing(count=count, parent="tool properties")

    def add_separate(self):
        add_separator(parent="tool properties")

    def add_instructions(self, value: str):
        add_spacing(count=2, parent=self.parent)
        add_text("How to use: ", parent=self.parent)
        add_spacing(count=1, parent=self.parent)
        add_text(value, parent=self.parent)