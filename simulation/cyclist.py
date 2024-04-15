from simulation.thing import Thing


class Cyclist(Thing):
    def __init__(self, speed, position, sprite, destination):
        self._init(speed, position, sprite, destination)
