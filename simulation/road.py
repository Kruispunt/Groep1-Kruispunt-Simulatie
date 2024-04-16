import json
from email.mime import image

from pygame import transform


class Road:
    def __init__(self, name):
        self._car_lanes = []
        self._cyclists_lanes = []
        self.pedestrian_lanes = []
        self._name = name

    def add_car_lane(self, lane):
        self._car_lanes.append(lane)

    def get_car_lanes(self):
        return self._car_lanes

    def get_cyclist_lanes(self):
        return self._cyclists_lanes

    def add_cyclist_lane(self, lane):
        self._cyclists_lanes.append(lane)

    def add_pedestrian_lane(self, lane):
        self.pedestrian_lanes.append(lane)

    def get_pedestrian_lanes(self):
        return self.pedestrian_lanes

    def get_name(self):
        return self._name

    def to_json(self):
        # serialize the object to json
        return {
            self._name: {
                "Cars":
                    [lane.to_json() for lane in self._car_lanes],
                "Cyclists":
                    [lane.to_json() for lane in self._cyclists_lanes],
                "Pedestrians":
                    [lane.to_json() for lane in self.pedestrian_lanes]
            }
        }

    def from_json(self, data):
        if self._name in data and "Cars" in data[self._name]:
            for i, lane in enumerate(self._car_lanes):
                lane.from_json(data[self._name]["Cars"][i])
        if self._name in data and "Cyclists" in data[self._name]:
            for i, lane in enumerate(self._cyclists_lanes):
                lane.from_json(data[self._name]["Cyclists"][i])
        if self._name in data and "Pedestrians" in data[self._name]:
            for i, lane in enumerate(self.pedestrian_lanes):
                lane.from_json(data[self._name]["Pedestrians"][i])
