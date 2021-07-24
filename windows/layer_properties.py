import dearpygui.dearpygui as dpg
from windows.base_window import *

layers = ["Layer 1"]
layer_ids = [dpg.generate_uuid()]
layer_count = 1
rename_layer_popup = None
rename_layer_text = None
layer_exists_error = None
layer_name_error = None

# Add the first drawing layer to the pad
dpg.add_draw_layer(id=layer_ids[0], parent=drawing_pad)


def add_layer():
    # Function runs when add_layer_button is pressed and adds a new layer
    global layers, layer_count, layer_ids

    layer_count += 1
    # Adds new layer to global list of layers
    layers.insert(0, f"Layer {layer_count}")
    layer_ids.insert(0, dpg.generate_uuid())

    # Adds new layer to the drawing pad
    dpg.add_draw_layer(id=layer_ids[0], parent=drawing_pad)

    # adds new layer and makes it active
    dpg.configure_item(item=active_layer, items=layers, default_value=f"Layer {layer_count}")


def remove_layer():
    # Function runs when remove_layer_button is pressed and removes the active layer
    global layers, layer_count, layer_ids

    layer_to_remove = dpg.get_value(item=active_layer)
    layer_position = layers.index(layer_to_remove)
    dpg.delete_item(item=layer_ids[layer_position])  # Remove the layer from the drawlist
    layers.remove(layer_to_remove)  # Remove layer from list
    layer_ids.pop(layer_position)  # Remove the id of layer

    # Remove layer from radio button list
    if layer_position != len(layers):  # Check if last layer item is being removed
        dpg.configure_item(item=active_layer, items=layers, default_value=layers[layer_position])
    else:
        dpg.configure_item(item=active_layer, items=layers, default_value=layers[layer_position-1])


def remove_layer_check():
    # Check if user is trying to remove the only layer present in the drawing
    if len(layers) == 1:
        dpg.configure_item(item=one_layer_error_popup, show=True)
    else:
        remove_layer()


def rename_layer():
    # Renames the layer in the global list and the radio button list
    global layers, rename_layer_popup, rename_layer_text, layer_name_error, layer_exists_error

    invalid_characters = ["\\", "/", ":", "?", "\"", "<", ">", "|"]
    layer_to_rename = dpg.get_value(item=active_layer)
    layer_position = layers.index(layer_to_rename)
    rename_layer_to = dpg.get_value(rename_layer_text)

    if layer_to_rename[:8] == "(hidden)":
        rename_layer_to = f"(hidden) {rename_layer_to}"

    if rename_layer_to == "":
        return

    if rename_layer_to in layers:
        if rename_layer_to != layer_to_rename:
            dpg.configure_item(item=layer_name_error, show=False)
            dpg.configure_item(item=layer_exists_error, show=True)
            return

    for character in rename_layer_to:
        if character in invalid_characters:
            dpg.configure_item(item=layer_exists_error, show=False)
            dpg.configure_item(item=layer_name_error, show=True)
            return

    layers[layer_position] = rename_layer_to
    dpg.configure_item(item=active_layer, items=layers, default_value=rename_layer_to)

    dpg.delete_item(rename_layer_popup)


def rename_layer_window():
    # Shows the window to rename layer
    global layers, rename_layer_popup, rename_layer_text, layer_exists_error, layer_name_error

    layer_to_rename = dpg.get_value(item=active_layer)

    if layer_to_rename[:8] == "(hidden)":
        layer_to_rename = layer_to_rename[9:]

    with dpg.window(label="Rename Layer",  modal=True, show=True, no_resize=True,
                    no_close=True, no_move=True, no_title_bar=False, autosize=True,
                    pos=[int(screen_width / 2) - 125, int(screen_height / 2) - 120]) as rename_layer_popup:

        dpg.set_item_theme(item=rename_layer_popup, theme=popup_theme)
        rename_layer_text = dpg.add_input_text(label="", default_value=layer_to_rename, width=210, on_enter=True,
                                               hint="Layer name cannot be empty", callback=rename_layer)

        layer_exists_error = dpg.add_text("Layer name already in use", show=False, color=(180, 0, 0))
        layer_name_error = dpg.add_text("Layer name cannot have \\ / : ? \" < >  |", show=False, wrap=220,
                                        color=(180, 0, 0))

        with dpg.group(horizontal=True):
            yes_rename_button = dpg.add_button(label="Rename", width=100, callback=rename_layer)
            no_rename_button = dpg.add_button(label="Cancel", width=100,
                                              callback=lambda: dpg.delete_item(rename_layer_popup))

        dpg.set_item_font(item=rename_layer_popup, font=bold_font)
        dpg.set_item_font(item=yes_rename_button, font=regular_font)
        dpg.set_item_font(item=no_rename_button, font=regular_font)
        dpg.set_item_font(item=rename_layer_text, font=regular_font)
        dpg.set_item_font(item=layer_exists_error, font=regular_font)
        dpg.set_item_font(item=layer_name_error, font=regular_font)


def hide_layer():
    global layers, layer_ids

    layer_selected = dpg.get_value(item=active_layer)
    if layer_selected[:8] == "(hidden)":
        return
    layer_position = layers.index(layer_selected)
    layers[layer_position] = f"(hidden) {layer_selected}"
    dpg.configure_item(item=layer_ids[layer_position], show=False)
    dpg.configure_item(item=active_layer, items=layers, default_value=layers[layer_position])


def show_layer():
    global layers, layer_ids

    layer_selected = dpg.get_value(item=active_layer)
    if layer_selected[:8] == "(hidden)":
        layer_position = layers.index(layer_selected)
        layers[layer_position] = layer_selected[9:]
        dpg.configure_item(item=layer_ids[layer_position], show=True)
        dpg.configure_item(item=active_layer, items=layers, default_value=layers[layer_position])


def move_layer_up():
    global layers, layer_ids
    layer_selected = dpg.get_value(item=active_layer)
    layer_position = layers.index(layer_selected)

    if layer_position != 0:
        dpg.move_item_down(item=layer_ids[layer_position])
        layers[layer_position], layers[layer_position-1] = layers[layer_position-1], layers[layer_position]
        layer_ids[layer_position], layer_ids[layer_position - 1] = layer_ids[layer_position - 1], layer_ids[layer_position]
        dpg.configure_item(item=active_layer, items=layers, default_value=layers[layer_position - 1])


def move_layer_down():
    global layers, layer_ids
    layer_selected = dpg.get_value(item=active_layer)
    layer_position = layers.index(layer_selected)

    if layer_position != len(layers)-1:
        dpg.move_item_up(item=layer_ids[layer_position])
        layers[layer_position], layers[layer_position + 1] = layers[layer_position + 1], layers[layer_position]
        layer_ids[layer_position], layer_ids[layer_position + 1] = layer_ids[layer_position + 1], layer_ids[layer_position]
        dpg.configure_item(item=active_layer, items=layers, default_value=layers[layer_position + 1])


# Record screen resolution
screen_width, screen_height = get_screen_resolution()

# Subtract Taskbar and title bar height
screen_height = screen_height - int(0.05*screen_height)

# Get image information and make textures
width_show, height_show, channels_show, data_show = dpg.load_image("icons/show_icon.png")
width_hide, height_hide, channels_hide, data_hide = dpg.load_image("icons/hide_icon.png")
width_add, height_add, channels_add, data_add = dpg.load_image("icons/add_icon.png")
width_remove, height_remove, channels_remove, data_remove = dpg.load_image("icons/remove_icon.png")
width_rename, height_rename, channels_rename, data_rename = dpg.load_image("icons/rename_icon.png")

with dpg.texture_registry():
    texture_id_show = dpg.add_static_texture(width_show, height_show, data_show)
    texture_id_hide = dpg.add_static_texture(width_hide, height_hide, data_hide)
    texture_id_add = dpg.add_static_texture(width_add, height_add, data_add)
    texture_id_remove = dpg.add_static_texture(width_remove, height_remove, data_remove)
    texture_id_rename = dpg.add_static_texture(width_rename, height_rename, data_rename)

with dpg.group(parent=layer_properties):
    layer_header = dpg.add_text("Drawing Layers")
    dpg.add_dummy()
    dpg.set_item_font(item=layer_header, font=bold_font)

    with dpg.group(horizontal=True):
        with dpg.child(autosize_y=True, width=int(0.134*screen_width)) as layer_list:
            dpg.set_item_theme(item=layer_list, theme=layer_list_theme)
            active_layer = dpg.add_radio_button(items=layers, default_value="Layer 1")

        with dpg.group():
            dpg.add_dummy()
            add_layer_button = dpg.add_image_button(texture_id_add, width=15, height=15, callback=add_layer)
            remove_layer_button = dpg.add_image_button(texture_id_remove, width=15, height=15,
                                                       callback=remove_layer_check)
            rename_layer_button = dpg.add_image_button(texture_id_rename, width=15, height=15,
                                                       callback=rename_layer_window)
            dpg.add_separator()
            show_layer_button = dpg.add_image_button(texture_id_show, width=15, height=15, callback=show_layer)
            hide_layer_button = dpg.add_image_button(texture_id_hide, width=15, height=15, callback=hide_layer)
            dpg.add_separator()
            move_layer_up_button = dpg.add_button(label="Button", width=15, height=15, arrow=True,
                                                  direction=dpg.mvDir_Up, callback=move_layer_up)
            move_layer_down_button = dpg.add_button(label="Button", width=15, height=15, arrow=True,
                                                    direction=dpg.mvDir_Down, callback=move_layer_down)

with dpg.window(label="Drawing must have at least one layer!",  modal=True, show=False, no_resize=True,
                no_close=True, no_move=True,
                pos=[int(screen_width / 2) - 125, int(screen_height / 2) - 120]) as one_layer_error_popup:

    dpg.set_item_theme(item=one_layer_error_popup, theme=popup_theme)
    dpg.add_dummy(height=5)
    ok_button = dpg.add_button(label="OK", width=300,
                               callback=lambda: dpg.configure_item(one_layer_error_popup, show=False))
    dpg.set_item_font(one_layer_error_popup, bold_font)
    dpg.set_item_font(item=ok_button, font=regular_font)
