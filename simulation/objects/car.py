from simulation.abstract_classes.thing import Thing


class Car(Thing):
    def __init__(self, speed, position, sprite, destination, size):
        self._init(speed, position, sprite, destination, size)