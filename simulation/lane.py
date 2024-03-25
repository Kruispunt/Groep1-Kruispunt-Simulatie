import json

from simulation.car import Car
from simulation.light import Light
from pygame import image, Vector2


class Lane:
    def __init__(self, direction, start_position, light_position):
        self._start_position = start_position
        self._light_position = light_position
        self._direction = direction
        self._light = Light()
        self._cars = []
        self._has_car_waiting = False
        self._has_priority_vehicle = False

    def get_start_position(self):
        return self._start_position

    def get_light_position(self):
        return self._light_position

    def get_direction(self):
        return self._direction

    def add_car(self):
        self._cars.append(Car(1, Vector2(self._start_position), self._light_position - self._start_position,
                              image.load("simulation/images/car.png")))

    def remove_car(self, car):
        self._cars.remove(car)

    def get_cars(self):
        return self._cars

    def has_car_waiting(self):
        return self._has_car_waiting

    def set_has_car_waiting(self, has_car_waiting):
        self._has_car_waiting = has_car_waiting

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
            "detectielus": self._has_car_waiting,
            "prioriteit": self._has_priority_vehicle,
        }
