from gi.repository import Gtk

class Seasons(Gtk.VBox):
    def __init__(self):
        Gtk.Box.__init__(self)

        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        
        season1 = self.init_season(None)
        

        stack.add_titled(season1, "Season 1", "Season 1")
        stack.add_titled(Gtk.Label("Season 2"), "Season 2", "Season 2")

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)

        self.pack_start(stack_switcher, False, False, 4)
        self.pack_start(stack, False, False, 0)

    def init_season(self, data):
        box = Gtk.Box()

        episode_list = Gtk.ListBox()
        episode_list.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
        episode_list.connect("row_selected", self.on_item_select)
        episode_list.connect("row_activated", self.on_item_click)

        episoda = Gtk.Label("Episoda")
        episoda.set_halign(Gtk.Align.START)
        episode_list.add(episoda)
        episode_list.add(Gtk.Label("Episoda"))
        episode_list.add(Gtk.Label("Episoda"))

        box.pack_start(episode_list, True, True, 0)
        return box

    def on_item_select(self, list_box, list_box_row):
        pass
        '''print("selected")
        index = list_box_row.get_index()
        selected_row = list_box.get_row_at_index(index)

        for i in range(0, index):
            list_box.select_row(
                list_box.get_row_at_index(i)
            )'''

    #list box row should represent store data, toggle episode watch in store and redraw(reselect) rows
    def on_item_click(self, list_box, list_box_row):
        print(list_box_row.is_selected())
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