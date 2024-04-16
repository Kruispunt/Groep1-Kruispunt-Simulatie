from pygame import image, transform

from simulation.abstract_classes.lane import Lane
from simulation.enums.state import State
from simulation.objects.pedestrian import Pedestrian


class Pedestrian_Lane(Lane):
    def __init__(self, start_position, inbetween_positions, light_position, connection=None, spawnable=True):
        self._init(start_position, inbetween_positions, light_position, connection, spawnable)

    def add_pedestrian(self, sprite=None):
        if sprite is None:
            sprite = image.load("simulation/images/pedestrian.png")
            # make sure the aspect ratio is correct, width is 50
        original_width, original_height = sprite.get_size()

        # Calculate the height while maintaining the aspect ratio
        scaled_width = int(20 * (original_width / original_height))
        sprite = transform.scale(sprite, (scaled_width, 20))

        thing_position = self._start_position.copy()

        if (self._things and self._start_position.dot(self._things[-1].get_position()) >= 0
                and self._things[-1].get_destination() == self._light_position):
            thing_position = self._things[-1].get_position() - (
                        self._light_position - self._start_position).normalize() * (
                               20 + 5)

        self._things.append(Pedestrian(1, thing_position, sprite, self._light_position))

    def to_json(self):
        return {
            "DetectPedestrians": self._has_waiting,
        }

    def from_json(self, data):
        self._light.change(State(data))
