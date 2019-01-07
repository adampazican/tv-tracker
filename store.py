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

    def getShowNames(self):
        return list(map(lambda x: x["name"], self.data))

    def getShowByName(self, name):
        return list(filter(lambda x: x["name"] == name, self.data))[0]
    
    def getShowById(self, show_id):
        return list(filter(lambda x: x["id"] == show_id, self.data))[0]

    def get_episode_watched(self, show_name, episode_name):
        for show in self.data:
            if show["name"] == show_name:
                for episode in show["episodes"]:
                    if episode["name"] == episode_name:
                        episode["watched"] = episode.get("watched", False)
                        return episode["watched"]

    #watched is boolean
    def set_episode_watched(self, show_name, episode_name, watched):
        for show in self.data:
            if show["name"] == show_name:
                for episode in show["episodes"]:
                    if episode["name"] == episode_name:
                        episode["watched"] = watched
                        self.save_store()
                        break
                break

    def set_temporary_data(self, data):
        self.temporary_data = data