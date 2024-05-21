from random import randint

from simulation.abstract_classes.lane import Lane
from simulation.light import Light
from simulation.objects.bus import Bus
from simulation.enums.state import State
from pygame import image, transform


class Bus_Lane(Lane):
    def __init__(self, start_position, inbetween_positions, light_position, connection=None, spawnable=True, linked_connection=None, linked_inbetween_positions=None, linked_light_position=None):
        self._init(start_position, inbetween_positions, light_position, connection, spawnable)
        self.linked_connection = linked_connection
        self._is_linked = linked_connection is not None
        self.linked_inbetween_positions = linked_inbetween_positions
        self.linked_light = Light() if self._is_linked else None
        self.linked_light_position = linked_light_position if self._is_linked else None
        self.going_alternative = False

    def is_linked(self):
        return self._is_linked

    def add_bus(self, number, going_linked_connection=False, connection=None, sprite=None):
        if connection is not None:
            self._connection = connection

        self.going_alternative = going_linked_connection

        if sprite is None:
            sprite = image.load("simulation/images/bus.png")
        # make sure the aspect ratio is correct
        original_width, original_height = sprite.get_size()

        # Calculate the height while maintaining the aspect ratio
        scaled_width = int(60 * (original_width / original_height))
        bus_image = transform.scale(sprite, (scaled_width, 60))

        position = self._start_position.copy()

        if (self._things and self._start_position.dot(self._things[-1].get_position()) >= 0
                and self._things[-1].get_destination() == self._light_position):
            position = self._things[-1].get_position() - (self._light_position - self._start_position).normalize() * (60 + 10)

        self._things.append(Bus(3, position, bus_image, self._light_position, number, 60))

    def set_linked_light(self, state):
        if self._is_linked:
            self.linked_light.change(state)

    def to_json(self):
        return 1

    def from_json(self, data):
        self._light.change(State(data))
