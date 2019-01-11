import os
import json
from urllib.request import urlopen

class Store():
    def __init__(self):
        if not os.path.exists("cache"):
            os.mkdir("cache")
        
        if not os.path.exists("cache/store.json"):
            with open("cache/store.json", "w"): pass
        
        with open("cache/store.json", "r") as store:
            self.data = json.loads(store.read())
        self.temporary_data = []

    def save_store(self):
        with open("cache/store.json", "w") as store:
            store.write(
                json.dumps(self.data, indent=4, separators=(',', ': '))
            )

    def get_shows(self):
        return self.data
    
    def get_show_by_id(self, show_id):
        data = list(filter(lambda x: x["id"] == show_id, self.data))
        if data:
            return data[0]
        return list(filter(lambda x: x["id"] == show_id, self.temporary_data))[0]

    def get_episode_watched(self, show_name, episode_name):
        for show in self.data:
            if show["name"] == show_name:
                for episode in show["episodes"]:
                    if episode["name"] == episode_name:
                        episode["watched"] = episode.get("watched", False)
                        return episode["watched"]

        for show in self.temporary_data:
            if show["name"] == show_name:
                for episode in show["episodes"]:
                    if episode["name"] == episode_name:
                        episode["watched"] = episode.get("watched", False)
                        return episode["watched"]

    def set_episode_watched(self, show_name, episode_name, is_watched):
        for show in self.data:
            if show["name"] == show_name:
                for episode in show["episodes"]:
                    if episode["name"] == episode_name:
                        episode["watched"] = is_watched
                        self.save_store()
                        break
                break

        for show in self.temporary_data:
            if show["name"] == show_name:
                for episode in show["episodes"]:
                    if episode["name"] == episode_name:
                        episode["watched"] = is_watched
                        self.save_store()
                        break
                break

    def set_temporary_episodes(self, data):
        self.temporary_data = list(map(lambda x: x["show"], data))

    def get_temporary_episodes(self):
        return self.temporary_data

    def fetch_episodes_for_show(self, show_id):
        for show in self.temporary_data:
            if show["id"] == show_id:
                if "episodes" in show:
                    break 
                url = urlopen("https://api.tvmaze.com/shows/%i/episodes" % show["id"]).read()
                data = json.loads(url.decode("utf-8"))
                show["episodes"] = data

                if not os.path.exists("cache/%i.jpg" % show["id"]):
                    if show["image"] != None:
                        self.cache_image(show["image"]["medium"], "cache/%i.jpg" % show["id"])
                    else:
                        self.cache_image('https://static.tvmaze.com/images/no-img/no-img-portrait-text.png', "cache/no-image.jpg")
                break

    def cache_image(self, url, path):
        response = urlopen(url)
        with open(path, "wb") as img:
            if response.getcode() == 200:
                img.write(response.read())

    def is_show_subscribed(self, show_id):
        for show in self.data:
            if show["id"] == show_id:
                return True
        return False

    def subscribe_show(self, show_id):
        for show in self.temporary_data:
            if show["id"] == show_id:
                self.data.append(show)
                self.save_store()

    def unsubscribe_show(self, show_id):
        for show in self.data:
            if show["id"] == show_id:
                self.data.remove(show)
                self.save_store()