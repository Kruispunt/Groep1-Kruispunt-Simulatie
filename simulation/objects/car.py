from simulation.abstract_classes.thing import Thing


class Car(Thing):
    def __init__(self, speed, position, sprite, destination, size, is_prio=False, connection=None, is_different=False):
        self.is_different = is_different
        self.is_priority = is_prio
        self._init(speed, position, sprite, destination, size, connection)
