import json

from pygame import image, display, transform


class Intersection:
    def __init__(self, name):
        self._name = name
        self.roads = []

    def get_name(self):
        return self._name

    def add_road(self, road):
        self.roads.append(road)

    def get_roads(self):
        return self.roads

    def to_json(self):
        json_structure = {}

        for road in self.roads:
            json_structure.update(road.to_json())

        return {self._name: json_structure}

    def from_json(self, message):
        for road in self.roads:
            road.from_json(message)