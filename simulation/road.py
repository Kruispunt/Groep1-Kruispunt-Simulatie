import json
from email.mime import image

from pygame import transform


class Road:
    def __init__(self, name):
        self._lanes = []
        self._cyclists = []
        self._name = name

    def add_lane(self, lane):
        self._lanes.append(lane)

    def get_lanes(self):
        return self._lanes

    def get_name(self):
        return self._name

    def to_json(self):
        # serialize the object to json
        return {
            self._name: {
                "Cars":
                    [lane.to_json() for lane in self._lanes]
            }
        }

    def from_json(self, data):
        if self._name in data and "Cars" in data[self._name]:
            for i, lane in enumerate(self._lanes):
                lane.from_json(data[self._name]["Cars"][i])
