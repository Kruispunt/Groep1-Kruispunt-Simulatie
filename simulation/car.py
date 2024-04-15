import math

from pygame import transform
from pygame.math import Vector2

from simulation.thing import Thing


class Car(Thing):
    def __init__(self, speed, position, sprite, destination):
        self._init(speed, position, sprite, destination)