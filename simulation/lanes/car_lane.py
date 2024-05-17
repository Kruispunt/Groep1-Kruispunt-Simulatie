from random import randint

from simulation.abstract_classes.lane import Lane
from simulation.objects.car import Car
from simulation.enums.state import State
from pygame import image, transform


class Car_Lane(Lane):
    def __init__(self, start_position, inbetween_positions, light_position, connection=None, spawnable=True):
        self._has_priority_vehicle = False
        self._has_car_waiting_far = False
        self._init(start_position, inbetween_positions, light_position, connection, spawnable)


    def has_waiting_far(self):
        return self._has_car_waiting_far

    def set_has_waiting_far(self, has_car_waiting_far):
        self._has_car_waiting_far = has_car_waiting_far

    def has_priority_vehicle(self):
        return self._has_priority_vehicle

    def set_has_priority_vehicle(self, has_priority_vehicle):
        self._has_priority_vehicle = has_priority_vehicle

    def add_bus(self, number, sprite=None):
        if sprite is None:
            sprite = image.load("simulation/images/car" + randint(0, 1).__str__() + ".png")
        # make sure the aspect ratio is correct, width is 50
        original_width, original_height = sprite.get_size()

        # Calculate the height while maintaining the aspect ratio
        scaled_width = int(60 * (original_width / original_height))
        car_image = transform.scale(sprite, (scaled_width, 60))

        position = self._light_position.copy() - (self._light_position - self._start_position).normalize() * 20

        self._things.append(Car(3, position, car_image, self._light_position, 60))

    def add_car(self, size, sprite=None):
        if sprite is None:
            sprite = image.load("simulation/images/car" + randint(0, 1).__str__() + ".png")
        # make sure the aspect ratio is correct, width is 50
        original_width, original_height = sprite.get_size()

        # Calculate the height while maintaining the aspect ratio
        scaled_width = int(size * (original_width / original_height))
        car_image = transform.scale(sprite, (scaled_width, size))

        position = self._start_position.copy()

        if (self._things and self._start_position.dot(self._things[-1].get_position()) >= 0
                and self._things[-1].get_destination() == self._light_position):
            position = self._things[-1].get_position() - (self._light_position - self._start_position).normalize() * (
                        size + 10)

        self._things.append(Car(3, position, car_image, self._light_position, size))

    def to_json(self):
        # make sure it doesn't produce a string
        return {
            "DetectNear": self._has_waiting,
            "DetectFar": self._has_car_waiting_far,
            "PrioCar": self._has_priority_vehicle,
        }

    def from_json(self, data):
        self._light.change(State(data))
