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


    def getShowNames(self):
        return list(map(lambda x: x["name"], self.data))

    def getShowByName(self, name):
        return list(filter(lambda x: x["name"] == name, self.data))[0]


