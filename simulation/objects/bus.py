from simulation.abstract_classes.thing import Thing


class Bus(Thing):
    def __init__(self, speed, position, sprite, destination, number, size, connection=None):
        self._init(speed, position, sprite, destination, size, connection)
        self._number = number

    def get_number(self):
        return self._number
