from simulation.abstract_classes.thing import Thing


class Cyclist(Thing):
    def __init__(self, speed, position, sprite, destination):
        self._init(speed, position, sprite, destination)
