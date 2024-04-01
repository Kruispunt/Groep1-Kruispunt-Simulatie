import json
from random import randint

from simulation.car import Car
from simulation.enums.state import State
from simulation.light import Light
from pygame import image, Vector2, transform


class Lane:
    def __init__(self, direction, start_position, inbetween_positions, light_position):
        if not inbetween_positions:
            assert False, "inbetween_positions is empty"

        self._start_position = start_position
        self._inbetween_positions = inbetween_positions
        self._light_position = light_position
        self._direction = direction
        self._light = Light()
        self._cars = []
        self._has_car_waiting = False
        self._has_car_waiting_far = False
        self._has_priority_vehicle = False

    def get_start_position(self):
        return self._start_position

    def get_inbetween_positions(self):
        return self._inbetween_positions

    def get_light_position(self):
        return self._light_position

    def get_direction(self):
        return self._direction

    def add_car(self):
        car_image = image.load("simulation/images/car" + randint(0, 1).__str__() + ".png")
        # make sure the aspect ratio is correct, width is 50
        original_width, original_height = car_image.get_size()

        # Calculate the height while maintaining the aspect ratio
        scaled_width = int(40 * (original_width / original_height))
        car_image = transform.scale(car_image, (scaled_width, 40))

        position = self._start_position.copy()

        if (self._cars and self._start_position.dot(self._cars[-1].get_position()) >= 0
                and self._cars[-1].get_destination() == self._light_position):
            position = self._cars[-1].get_position() - (self._light_position - self._start_position).normalize() * (40 + 10)

        self._cars.append(Car(2.5, position, car_image, self._light_position))

    def remove_car(self, car):
        self._cars.remove(car)

    def get_cars(self):
        return self._cars

    def has_car_waiting(self):
        return self._has_car_waiting

    def set_has_car_waiting(self, has_car_waiting):
        self._has_car_waiting = has_car_waiting

    def has_car_waiting_far(self):
        return self._has_car_waiting_far

    def set_has_car_waiting_far(self, has_car_waiting_far):
        self._has_car_waiting_far = has_car_waiting_far

    def has_priority_vehicle(self):
        return self._has_priority_vehicle

    def set_has_priority_vehicle(self, has_priority_vehicle):
        self._has_priority_vehicle = has_priority_vehicle

    def get_light(self):
        return self._light

    def is_car_at_light(self, car):
        # only check if car is in front of light
        distance = car.get_position().distance_to(self._light_position)
        dot = car.get_direction().dot(self._light_position - car.get_position())
        if distance < 10 and dot > 0:
            return True
        return False

    def to_json(self):
        # make sure it doesn't produce a string
        return {
            "DetectNear": self._has_car_waiting,
            "DetectFar": self._has_car_waiting_far,
            "PrioCar": self._has_priority_vehicle,
        }

    def from_json(self, data):
        self._light.change(State(data))
