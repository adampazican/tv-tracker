import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from sidebar import Sidebar
from showinfo import ShowInfo
from store import Store


class Application(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.connect("destroy", Gtk.main_quit)
        self.set_default_size(1000, 600)
        self.load_css()

        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)
        header_bar.props.title = "TVTracker"

        search_button = Gtk.ToggleButton()
        search_icon = Gtk.Image.new_from_icon_name("edit-find-symbolic", 4)

        search_button.add(search_icon)
        header_bar.pack_start(search_button)
        self.set_titlebar(header_bar)

        self.store = Store()

        box = Gtk.Box(Gtk.Orientation.HORIZONTAL)

        self.sidebar = Sidebar(self.store, search_button)
        self.sidebar.connect("notify::selected-show", self.on_navigation_change)

        separator = Gtk.Separator()
        self.show_info = ShowInfo(self.store)
        self.show_info.connect("subscription_changed", self.on_subscription_change)

        box.pack_start(self.sidebar, False, False, 0)
        box.pack_start(separator, False, False, 0)
        box.pack_start(self.show_info, True, True, 0)
        self.add(box)

    def on_subscription_change(self, show_info_component, show_id, is_subscribed):
        show = self.store.get_show_by_id(show_id)

        if is_subscribed == True:
            self.sidebar.add_item(show)
        else:
            self.sidebar.remove_item(show)
    
    def on_navigation_change(self, sidebar, selected_show_prop):
        selected_show_id = sidebar.get_property("selected_show") 
        selected_show = self.store.get_show_by_id(selected_show_id)
        is_subscribed = self.store.is_show_subscribed(selected_show_id)

        self.show_info.set_id(selected_show["id"])
        self.show_info.set_name(selected_show["name"])
        self.show_info.set_status(selected_show["status"])
        self.show_info.set_rating(selected_show["rating"]["average"])
        self.show_info.set_summary(selected_show["summary"])
        self.show_info.set_genre(selected_show["genres"])
        self.show_info.set_episodes(selected_show["episodes"])
        self.show_info.set_subscribed(is_subscribed)

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
    window.maximize()
    Gtk.main()