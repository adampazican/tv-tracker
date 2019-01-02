from gi.repository import Gtk, GObject
from gi.repository.GdkPixbuf import Pixbuf
from urllib.request import urlopen
from seasons import Seasons
import re

class ShowInfo(Gtk.VBox):
    id_prop = GObject.Property(type=int, flags = GObject.ParamFlags.READWRITE)
    name_prop = GObject.Property(type=str, flags = GObject.ParamFlags.READWRITE)
    #genre
    status_prop = GObject.Property(type=str, flags = GObject.ParamFlags.READWRITE)
    rating_prop = GObject.Property(type=int, flags = GObject.ParamFlags.READWRITE)
    summary_prop = GObject.Property(type=str, flags = GObject.ParamFlags.READWRITE)

    def __init__(self):
        Gtk.Box.__init__(self)

        self.get_style_context().add_class("show-info")

        wrapper = Gtk.HBox()
        wrapper.set_spacing(8)
        
        info_box = Gtk.VBox()
        info_box.get_style_context().add_class("info-box")
        info_box_wrapper = Gtk.VBox()
        info_box_wrapper.pack_start(info_box, True, False, 0)

        
        self.image = Gtk.Image()
        self.getImage()
        #self.getImage(image, "https://static.tvmaze.com/uploads/images/original_untouched/167/418968.jpg", "image.jpg")

        wrapper.pack_start(self.image, False, False, 0)
        wrapper.pack_start(info_box_wrapper, False, False, 0)


        self.name = Gtk.Label("Name: %s" % self.name_prop, halign=Gtk.Align.START)
        self.genre = Gtk.Label("Genre: Drama, Romance", halign=Gtk.Align.START)
        self.status = Gtk.Label("Status: %s" % self.status_prop, halign=Gtk.Align.START)
        self.rating = Gtk.Label("Rating: %i" % self.rating_prop, halign=Gtk.Align.START)
        self.summ = Gtk.Label("Summary:", halign=Gtk.Align.START)
        self.summ.get_style_context().add_class("summary")
        self.summary = Gtk.Label(self.summary_prop, halign=Gtk.Align.START)
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


        seasons = Seasons()
        

        self.add(wrapper)
        self.add(seasons)

    def set_name(self, value):
        self.name_prop = value
        self.name.set_label("Name: %s" % self.name_prop)
        self.getImage()

    def set_status(self, value):
        self.status_prop = value
        self.status.set_label("Status: %s" % self.status_prop)

    def set_rating(self, value):
        self.rating_prop = value
        self.rating.set_label("Rating: %i" % self.rating_prop)

    def set_summary(self, value):
        self.summary_prop = re.sub(r"<\/?[a-z+]>", "", value)
        self.summary.set_label(self.summary_prop)

    def getImage(self):
        # fuj
        if self.id_prop == 0:
            return 
        pb = Pixbuf.new_from_file_at_scale(filename = "cache/%i.jpg" % self.id_prop, width = 300, height = 300, preserve_aspect_ratio=True)
        self.image.set_from_pixbuf(pb)

    #self.getImage(image, "https://static.tvmaze.com/uploads/images/original_untouched/167/418968.jpg", "image.jpg")
    def cacheImage(self, image, url, name):
        response = urlopen(url)
        with open(name, "wb") as img:
            img.write(response.read())
        
        pb = Pixbuf.new_from_file_at_scale(filename = name, width = 300, height = 300, preserve_aspect_ratio=True)
        image.set_from_pixbuf(pb)