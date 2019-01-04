from gi.repository import Gtk, GObject

class Seasons(Gtk.Box):
    __gsignals__ = {
        "episode_selected": (GObject.SIGNAL_RUN_FIRST, None, (str,))
    }

    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.get_style_context().add_class("seasons")

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_propagate_natural_height(True)

        self.stack_switcher = Gtk.StackSwitcher()
        self.stack_switcher.set_stack(self.stack)
        scrolled.add(self.stack_switcher)

        self.pack_start(scrolled, False, False, 0)
        self.pack_start(self.stack, True, True, 0)

    def set_episodes(self, episodes):
        self.reset()

        for season_number, episodes in episodes.items():
            scrolled = Gtk.ScrolledWindow()

            episode_list = Gtk.ListBox()
            episode_list.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
            episode_list.connect("row_activated", self.on_item_click)

            scrolled.add(episode_list)
            scrolled.show_all()

            for episode in episodes:
                label = Gtk.Label(episode["name"], halign=Gtk.Align.START)
                label.show()
                episode_list.add(label)
                
                if "watched" in episode:
                    episode_list.select_row(episode_list.get_children()[-1])

            self.stack.add_titled(scrolled, "Season %i" % season_number, "Season %i" % season_number)

    def reset(self):
        for child in self.stack.get_children():
            self.stack.remove(child)

    #list box row should represent store data, toggle episode watch in store and redraw(reselect) rows
    def on_item_click(self, list_box, list_box_row):
        episode_name = list_box_row.get_children()[0].get_label()
        self.emit("episode_selected", episode_name)
        
        
        '''
        index = list_box_row.get_index()
        selected_row = list_box.get_row_at_index(index)

        if not list_box_row.is_selected():
            print("jej")
            for i in range(0, index):
                list_box.select_row(
                    list_box.get_row_at_index(i)
                )
        else:
            list_box.unselect_row(selected_row)
        '''