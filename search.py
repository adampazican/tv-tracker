from gi.repository import Gtk, GObject
from urllib.request import urlopen
import json

class Search(Gtk.Revealer):
    def __init__(self, store):
        Gtk.Revealer.__init__(self)
        self.store = store
        
        self.listbox = Gtk.ListBox()

        entry = Gtk.SearchEntry()
        entry.connect("activate", self.on_search_activate)

        entry_row = Gtk.ListBoxRow()
        entry_row.get_style_context().add_class("row")
        entry_row.set_selectable(False)
        entry_row.add(entry)

        self.listbox.add(entry_row)


        self.contain = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.contain.add(self.listbox)

        self.add(self.contain)
        
    def get_listbox(self):
        return self.listbox

    def on_search_activate(self, entry):
        url = urlopen("https://api.tvmaze.com/search/shows?q=%s" % entry.get_text()).read()
        data = json.loads(url.decode("utf-8"))
        self.store.set_temporary_episodes(data)

        self.show_results(self.store.get_temporary_episodes())

    def show_results(self, shows):
        self.clean_up_search()

        for show in shows:
            name = show["name"]
            row = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            row.id = show["id"]
            row.get_style_context().add_class("row")
            row.pack_start(Gtk.Label(name, halign=Gtk.Align.START), False, False, 0)
            self.listbox.add(row)
            
        if len(shows) > 0:
            self.contain.add(Gtk.Separator())
        self.contain.show_all()

    def clean_up_search(self):
        children = self.listbox.get_children()

        for child in children:
            if child.get_index() > 0:
                self.listbox.remove(child)
        
        for child in self.contain.get_children():
            if not type(child) == Gtk.ListBox:
                self.contain.remove(child)