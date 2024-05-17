import json
from email.mime import image

from pygame import transform


class Road:
    def __init__(self, name):
        self.car_lanes = []
        self.cyclists_lanes = []
        self.pedestrian_lanes = []
        self.bus_lanes = []
        self._name = name

    def add_bus_lane(self, lane):
        self.bus_lanes.append(lane)

    def get_bus_lanes(self):
        return self.bus_lanes

    def add_car_lane(self, lane):
        self.car_lanes.append(lane)

    def get_car_lanes(self):
        return self.car_lanes

    def get_cyclist_lanes(self):
        return self.cyclists_lanes

    def add_cyclist_lane(self, lane):
        self.cyclists_lanes.append(lane)

    def add_pedestrian_lane(self, lane):
        self.pedestrian_lanes.append(lane)

    def get_pedestrian_lanes(self):
        return self.pedestrian_lanes

    def get_name(self):
        return self._name

    def to_json(self):
        # serialize the object to json

        json_data = {}

        if self.car_lanes:
            json_data["Cars"] = [lane.to_json() for lane in self.car_lanes]

        if self.cyclists_lanes:
            json_data["Cyclists"] = [lane.to_json() for lane in self.cyclists_lanes]

        if self.pedestrian_lanes:
            json_data["Pedestrians"] = [lane.to_json() for lane in self.pedestrian_lanes]

        if self.bus_lanes:
            json_data["Busses"] = [lane.to_json() for lane in self.bus_lanes]

        return {self._name: json_data}

    def from_json(self, data):
        if self._name in data and "Cars" in data[self._name]:
            for i, lane in enumerate(self.car_lanes):
                lane.from_json(data[self._name]["Cars"][i])
        if self._name in data and "Cyclists" in data[self._name]:
            for i, lane in enumerate(self.cyclists_lanes):
                lane.from_json(data[self._name]["Cyclists"][i])
        if self._name in data and "Pedestrians" in data[self._name]:
            for i, lane in enumerate(self.pedestrian_lanes):
                lane.from_json(data[self._name]["Pedestrians"][i])
        if self._name in data and "Busses" in data[self._name]:
            for i, lane in enumerate(self.bus_lanes):
                lane.from_json(data[self._name]["Busses"][i])
