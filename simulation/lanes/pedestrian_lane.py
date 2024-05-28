from pygame import image, transform

from simulation.abstract_classes.lane import Lane
from simulation.enums.state import State
from simulation.objects.pedestrian import Pedestrian


class Pedestrian_Lane(Lane):
    def __init__(self, start_position, inbetween_positions, light_position, inbetween_light_positions=None,
                 connection=None, spawnable=True, split=None):
        if inbetween_light_positions is None:
            inbetween_light_positions = []
        self.inbetween_light_positions = inbetween_light_positions
        self.split = split
        self._init(start_position, inbetween_positions, light_position, connection, spawnable)

    def add_pedestrian(self, sprite=None):
        size = 15
        if sprite is None:
            sprite = image.load("simulation/images/pedestrian.png")
            # make sure the aspect ratio is correct, width is 50
        original_width, original_height = sprite.get_size()

        # Calculate the height while maintaining the aspect ratio
        scaled_width = int(size * (original_width / original_height))
        sprite = transform.scale(sprite, (scaled_width, size))

        thing_position = self._start_position.copy()

        if (self._things and abs(
                self._start_position.dot(self._things[-1].get_position())) >= 0 and self._start_position.distance_to(
                self._things[-1].get_position()) <= size
                and self._things[-1].get_destination() == self._light_position):
            thing_position = self._things[-1].get_position() - (
                    self._light_position - self._start_position).normalize() * (
                                     size + 5)

        inbetween_start_and_light = self._light_position.copy() if self.inbetween_light_positions == [] else self.inbetween_light_positions[0].copy()
        self._things.append(Pedestrian(1.5, thing_position, sprite, destination=inbetween_start_and_light, size=size))

    def to_json(self):
        return {
            "DetectPedestrians": self._has_waiting,
        }

    def from_json(self, data):
        self._light.change(State(data))
