import json

from pygame import image, display, transform


class Intersection:
    def __init__(self, width, height, name):
        self._name = name
        self._background = image.load("simulation/images/background.png")
        self._width = width
        self._height = height

        self._background = transform.scale(self._background, (width, height))
        self.roads = []

    def add_road(self, road):
        self.roads.append(road)

    def get_roads(self):
        return self.roads

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_background(self):
        return self._background

    def to_json(self):
        json_structure = {}

        for road in self.roads:
            json_structure.update(road.to_json())

        return json.dumps({self._name: json_structure})

    def from_json(self, message):
        data = json.loads(message)
        for road in self.roads:
            road.from_json(data[self._name])