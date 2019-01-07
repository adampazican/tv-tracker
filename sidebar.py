from gi.repository import Gtk, GObject
from search import Search

class Sidebar(Gtk.ScrolledWindow):
    selected_show = GObject.Property(type=str, flags = GObject.ParamFlags.READWRITE)

    def __init__(self, store):
        Gtk.ScrolledWindow.__init__(self, None, None)
        self.set_propagate_natural_width(True)
        self.store = store
        
        self.__list_box = Gtk.ListBox()
        self.__list_box.connect("row_selected", self.on_item_select)
        self.__list_box.get_style_context().add_class("sidebar")

        search = Search(self.store)
        search.connect("row_selected", self.on_search_select)

        listbox_row = Gtk.ListBoxRow()
        listbox_row.set_selectable(False)
        
        listbox_row.add(search)

        self.__list_box.add(listbox_row)

        self.add(self.__list_box)

        self.add_items(self.store.getShowNames())

    def add_items(self, show_names):
        for name in show_names:
            row = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            row.get_style_context().add_class("row")
            row.pack_start(Gtk.Label(name, halign=Gtk.Align.START), False, False, 0)
            self.__list_box.add(row)
        self.__list_box.select_row(
            self.__list_box.get_children()[1]
        )

    def on_item_select(self, list_box, list_box_row):
        self.selected_show = list_box_row.get_child().get_children()[0].get_label()

    def on_search_select(self, list_box, list_box_row):
        show_name = list_box_row.get_child().get_children()[0].get_label()
        self.store.get_episodes_for_show(show_name)
        self.selected_show = show_name
