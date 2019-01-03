from gi.repository import Gtk, GObject
from gi.repository.GdkPixbuf import Pixbuf
from urllib.request import urlopen
from seasons import Seasons
import re
import os

class ShowInfo(Gtk.Box):
    id = 0
    subscribed = True

    def __init__(self, store):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.get_style_context().add_class("show-info")

        self.store = store

        wrapper = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        wrapper.set_spacing(8)
        
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        info_box.get_style_context().add_class("info-box")
        info_box_wrapper = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        info_box_wrapper.pack_start(info_box, True, False, 0)

        
        self.image = Gtk.Image()
        self.getImage()

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
        subscription_button = Gtk.Button("Subscribe")
        subscription.pack_start(subscription_button, False, False, 0)

        info_box.pack_start(self.name, False, False, 0)
        info_box.pack_start(self.genre, False, False, 0)
        info_box.pack_start(self.status, False, False, 0)
        info_box.pack_start(self.rating, False, False, 0)
        info_box.pack_start(self.summ, False, False, 0)
        info_box.pack_start(self.summary, False, False, 0)
        info_box.pack_start(subscription, False, False, 0)

        self.seasons = Seasons()

        self.pack_start(wrapper, True, True, 0)
        self.pack_start(self.seasons, True, True, 0)

    def set_id(self, value):
        self.id = value

    def set_name(self, value):
        self.name.set_label("Name: %s" % value)
        self.getImage()

    def set_status(self, value):
        self.status.set_label("Status: %s" % value)

    def set_rating(self, value):
        self.rating.set_label("Rating: %.1f" % value)

    def set_summary(self, value):
        summary_without_markdown = re.sub(r"<\/?[a-z+]>", "", value)
        self.summary.set_label(summary_without_markdown)

    def set_genre(self, value):
        genres_unlistified = re.sub(r"\[?']?", "", str(value))
        self.genre.set_label("Genre: %s" % genres_unlistified)

    def set_episodes(self, value):
        seasons = {}

        for episode in value:
            season_number = episode["season"]
            
            if not season_number in seasons:
                seasons[season_number] = [episode]
            else:
                seasons[season_number].append(episode)

        self.seasons.set_episodes(seasons)

    def getImage(self):
        if os.path.exists("cache/%i.jpg" % self.id):
            pb = Pixbuf.new_from_file_at_scale(filename = "cache/%i.jpg" % self.id, width = 300, height = 300, preserve_aspect_ratio=True)
            self.image.set_from_pixbuf(pb)

    #self.getImage(image, "https://static.tvmaze.com/uploads/images/original_untouched/167/418968.jpg", "image.jpg")
    def cacheImage(self, image, url, name):
        response = urlopen(url)
        with open(name, "wb") as img:
            img.write(response.read())
        
        pb = Pixbuf.new_from_file_at_scale(filename = name, width = 300, height = 300, preserve_aspect_ratio=True)
        image.set_from_pixbuf(pb)