from simulation.abstract_classes.thing import Thing


class Bus(Thing):
    def __init__(self, speed, position, sprite, destination, number, size):
        self._init(speed, position, sprite, destination, size)
        self._number = number

    def get_number(self):
        return self._number
