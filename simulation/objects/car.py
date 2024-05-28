from simulation.abstract_classes.thing import Thing


class Car(Thing):
    def __init__(self, speed, position, sprite, destination, size, is_prio=False, connection=None):
        self.is_priority = is_prio
        self._init(speed, position, sprite, destination, size, connection)
