import json


class Road:
    def __init__(self, name):
        self._lanes = []
        self._name = name

    def add_lane(self, lane):
        self._lanes.append(lane)

    def get_lanes(self):
        return self._lanes

    def get_name(self):
        return self._name

    def to_json(self):
        # serialize the object to json
        return json.dumps({
            self._name: [lane.to_json() for lane in self._lanes]
        }, indent=4)
