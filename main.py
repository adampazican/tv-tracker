import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from sidebar import Sidebar
from showinfo import ShowInfo
from store import Store


class Application(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.title = "DDD"
        self.connect("destroy", Gtk.main_quit)
        self.set_default_size(1000, 600)
        self.load_css()

        self.store = Store()

        box = Gtk.Box(Gtk.Orientation.HORIZONTAL)

        
        sidebar = Sidebar(self.store)
        sidebar.connect("notify::selected-show", self.on_navigation_change)

        separator = Gtk.Separator()
        self.mainframe = ShowInfo(self.store)

        box.pack_start(sidebar, False, False, 0)
        box.pack_start(separator, False, False, 0)
        box.pack_start(self.mainframe, True, True, 0)
        self.add(box)
    
    def on_navigation_change(self, sidebar, selected_show_prop):
        selected_show_name = sidebar.get_property("selected_show") 
        selected_show = self.store.getShowByName(selected_show_name)

        self.mainframe.set_id(selected_show["id"])
        self.mainframe.set_name(selected_show["name"])
        self.mainframe.set_status(selected_show["status"])
        self.mainframe.set_rating(selected_show["rating"]["average"])
        self.mainframe.set_summary(selected_show["summary"])
        self.mainframe.set_genre(selected_show["genres"])
        self.mainframe.set_episodes(selected_show["episodes"])

    def load_css(self):
        style_provider = Gtk.CssProvider()

        css = open('style.css', 'rb')
        data = css.read()
        css.close()

        style_provider.load_from_data(data)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


if __name__ == "__main__":
    window = Application()
    window.show_all()
    Gtk.main()