from simulation.enums.state import State


class Light:
    def __init__(self):
        self._state = State.red

    def change(self, light_state):
        self._state = light_state

    def get_state(self):
        return self._state
