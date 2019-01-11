from gi.repository import Gtk, GObject
from search import Search

class Sidebar(Gtk.ScrolledWindow):
    selected_show = GObject.Property(type=int, flags = GObject.ParamFlags.READWRITE)

    def __init__(self, store, search_button):
        Gtk.ScrolledWindow.__init__(self, None, None)
        self.set_propagate_natural_width(True)
        self.store = store

        search_button.connect("toggled", self.search_toggled)
        
        self.__list_box = Gtk.ListBox()
        self.__list_box.connect("row_selected", self.on_item_select)
        self.__list_box.get_style_context().add_class("sidebar")

        self.search = Search(self.store)
        self.search.get_listbox().connect("row_selected", self.on_search_select)
        

        listbox_row = Gtk.ListBoxRow()
        listbox_row.set_selectable(False)
        
        listbox_row.add(self.search)

        self.__list_box.add(listbox_row)

        self.add(self.__list_box)

        self.add_items(self.store.get_shows())

        self.__list_box.select_row(
            self.__list_box.get_children()[1]
        )

    def search_toggled(self, search_button):
        self.search.set_reveal_child(
            not self.search.get_reveal_child()
        )

    def remove_item(self, show):
        for row in self.__list_box.get_children():
            box = row.get_child()

            if type(box) == Gtk.Box and box.id == show["id"]:
                self.__list_box.remove(row)

    def add_item(self, show):
        row = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        row.id = show["id"]
        row.get_style_context().add_class("row")
        row.pack_start(Gtk.Label(show["name"], halign=Gtk.Align.START), False, False, 0)
        row.show_all()
        self.__list_box.add(row)
    
    def add_items(self, shows):
        for show in shows:
            row = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            row.id = show["id"]
            row.get_style_context().add_class("row")
            row.pack_start(Gtk.Label(show["name"], halign=Gtk.Align.START), False, False, 0)
            row.show_all()
            self.__list_box.add(row)

    def on_item_select(self, list_box, list_box_row):
        if list_box_row:
            self.selected_show = list_box_row.get_child().id
            self.unselect_list(self.search.get_listbox())

    def on_search_select(self, list_box, list_box_row):
        if list_box_row:
            show_id = list_box_row.get_child().id
            self.store.fetch_episodes_for_show(show_id)
            self.selected_show = show_id
            self.unselect_list(self.__list_box)


    def unselect_list(self, list_box):
        for row in list_box.get_children():
            if row.is_selected():
                list_box.unselect_row(row)
