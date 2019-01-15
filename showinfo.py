from gi.repository import Gtk, GObject
from gi.repository.GdkPixbuf import Pixbuf
from urllib.request import urlopen
from seasons import Seasons
import re
import os

class ShowInfo(Gtk.Box):
    __gsignals__ = {
        "subscription_changed": (GObject.SIGNAL_RUN_FIRST, None, (int, bool,))
    }

    id = 0
    subscribed = True

    def __init__(self, store):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.get_style_context().add_class("show-info")

        self.store = store

        wrapper = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        wrapper.get_style_context().add_class("info-box-wrapper")
        wrapper.set_spacing(8)
        
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        info_box.get_style_context().add_class("info-box")
        info_box_wrapper = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        info_box_wrapper.pack_start(info_box, True, False, 0)

        
        self.image = Gtk.Image()
        self.get_image()

        wrapper.pack_start(self.image, False, False, 0)
        wrapper.pack_start(info_box_wrapper, False, False, 0)


        self.name = Gtk.Label(halign=Gtk.Align.START)
        self.genre = Gtk.Label(halign=Gtk.Align.START)
        self.status = Gtk.Label(halign=Gtk.Align.START)
        self.rating = Gtk.Label(halign=Gtk.Align.START)
        self.summ = Gtk.Label("", halign=Gtk.Align.START)
        self.summ.get_style_context().add_class("summary")
        self.summary = Gtk.Label(halign=Gtk.Align.START)
        self.summary.set_line_wrap(True)

        subscription = Gtk.Box()
        self.subscription_button = Gtk.Button()
        self.subscription_button.connect("clicked", self.on_subscribe_clicked)
        
        self.update_button = Gtk.Button("Update")
        self.update_button.connect("clicked", self.on_update_clicked)

        subscription.pack_start(self.subscription_button, False, False, 0)
        subscription.pack_start(self.update_button, False, False, 8)

        info_box.pack_start(self.name, False, False, 0)
        info_box.pack_start(self.genre, False, False, 0)
        info_box.pack_start(self.status, False, False, 0)
        info_box.pack_start(self.rating, False, False, 0)
        info_box.pack_start(self.summ, False, False, 0)
        info_box.pack_start(self.summary, False, False, 0)
        info_box.pack_start(subscription, False, False, 0)

        self.seasons = Seasons()
        self.seasons.connect("episode_selected", self.on_episode_selected)

        self.pack_start(wrapper, False, True, 0)
        self.pack_start(self.seasons, True, True, 0)

    def on_episode_selected(self, seasons, episode_name, list_box, list_box_row):
        episode_watched = self.store.get_episode_watched(self.store.get_show_by_id(self.id)["name"], episode_name)

        if not episode_watched:
            list_box_row.get_style_context().add_class("episode-watched")
        else:
            list_box_row.get_style_context().remove_class("episode-watched")

        self.store.set_episode_watched(
            self.store.get_show_by_id(self.id)["name"],
            episode_name,
            not episode_watched
        )

    def set_id(self, value):
        self.id = value

    def set_name(self, value):
        self.name.set_label("Name: %s" % value)
        self.get_image()

    def set_status(self, value):
        if value:
            self.status.set_label("Status: %s" % value)
        else:
            self.status.set_label("Status: none")

    def set_rating(self, value):
        if value:
            self.rating.set_label("Rating: %.1f" % value)
        else:
            self.rating.set_label("Rating: none")

    def set_summary(self, value):
        if value == None:
            self.summary.set_label("No summary for %s yet." % self.name.get_label()[6:])
        else:
            summary_without_markdown = re.sub(r"<\/?[a-z]+(?: \/)?>", "", value)
            self.summary.set_label(summary_without_markdown)

    def set_genre(self, value):
        if value:
            genres_unlistified = re.sub(r"\[?']?", "", str(value))
            self.genre.set_label("Genre: %s" % genres_unlistified)
        else:
            self.genre.set_label("Genre: none")

    def set_episodes(self, episodes):
        seasons = {}

        for episode in episodes:
            season_number = episode["season"]
            
            if not season_number in seasons:
                seasons[season_number] = [episode]
            else:
                seasons[season_number].append(episode)

        self.seasons.set_episodes(seasons)

    def get_image(self):
        path = ""
        if os.path.exists("cache/%i.jpg" % self.id):
            path = "cache/%i.jpg" % self.id
        elif os.path.exists("cache/temp_%i.jpg" % self.id):
            path = "cache/temp_%i.jpg" % self.id
        elif os.path.exists("cache/no-image.jpg"):
            path = "cache/no-image.jpg"
        else: 
            return
        pb = Pixbuf.new_from_file_at_scale(filename = path, width = 300, height = 300, preserve_aspect_ratio=True)
        self.image.set_from_pixbuf(pb)

    def set_subscribed(self, is_subscribed):
        self.is_subscribed = is_subscribed

        if is_subscribed:
            self.subscription_button.set_label("UnSubscribe")
            self.update_button.show()
        else:
            self.subscription_button.set_label("Subscribe")
            self.update_button.hide()

    def on_subscribe_clicked(self, button):
        if self.is_subscribed:
            self.emit("subscription_changed", self.id, False)
            self.store.unsubscribe_show(self.id)
            self.set_subscribed(False)
        else:
            self.emit("subscription_changed", self.id, True)
            self.store.subscribe_show(self.id)
            self.set_subscribed(True)

    def on_update_clicked(self, button):
        updated_show = self.store.update_show(self.id)

        self.set_name(updated_show["name"])
        self.set_status(updated_show["status"])
        self.set_rating(updated_show["rating"]["average"])
        self.set_summary(updated_show["summary"])
        self.set_genre(updated_show["genres"])
        self.set_episodes(updated_show["episodes"])