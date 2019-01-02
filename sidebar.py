from gi.repository import Gtk, GObject

class Sidebar(Gtk.ScrolledWindow):
    selected_show = GObject.Property(type=str, flags = GObject.ParamFlags.READWRITE)

    def __init__(self):
        Gtk.ScrolledWindow.__init__(self, None, None)
        self.set_propagate_natural_width(True)
        
        self.__list_box = Gtk.ListBox()
        self.__list_box.connect("row_selected", self.onItemSelect)
        self.__list_box.get_style_context().add_class("sidebar")

        listbox_row = Gtk.ListBoxRow()
        listbox_row.set_selectable(False)
        entry = Gtk.Entry()
        
        listbox_row.add(entry)
        self.__list_box.add(listbox_row)

        self.add(self.__list_box)

    def add_items(self, show_names):
        for name in show_names:
            row = Gtk.HBox()
            row.get_style_context().add_class("row")
            row.pack_start(Gtk.Label(name), False, False, 0)
            self.__list_box.add(row)

    def onItemSelect(self, list_box, list_box_row):
        self.selected_show = list_box_row.get_child().get_children()[0].get_label()
