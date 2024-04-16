from abc import ABC, abstractmethod

from simulation.light import Light


class Lane(ABC):
    def _init(self, start_position, inbetween_positions, light_position, connection=None, spawnable=True):
        if not inbetween_positions:
            assert False, "inbetween_positions is empty"
        self._start_position = start_position
        self._inbetween_positions = inbetween_positions
        self._light_position = light_position
        self._connection = connection
        self._light = Light()
        self._things = []
        self._has_waiting = False
        self._spawnable = spawnable

    def get_start_position(self):
        return self._start_position

    def get_inbetween_positions(self):
        return self._inbetween_positions

    def get_light_position(self):
        return self._light_position

    def get_connection(self):
        return self._connection

    def is_spawnable(self):
        """
        Check if it is a lane or a connection
        :return:
        """
        return self._spawnable

    def remove(self, thing):
        self._things.remove(thing)

    def get_all(self):
        return self._things

    def has_waiting(self):
        return self._has_waiting

    def set_has_waiting(self, has_car_waiting):
        self._has_waiting = has_car_waiting

    def change_light(self, state):
        self._light.change(state)

    def light_state(self):
        return self._light.get_state()

    def is_at_light(self, thing):
        # only check if car is in front of light
        distance = thing.get_position().distance_to(self._light_position)
        dot = thing.get_direction().dot(self._light_position - thing.get_position())
        if distance < 10 and dot > 0:
            return True
        return False

    @abstractmethod
    def to_json(self):
        pass

    @abstractmethod
    def from_json(self, data):
        pass
