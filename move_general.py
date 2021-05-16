import numpy as np
import colorama as col

from general import General
import config


class MoveGeneral(General):
    def __init__(self, figure, position, color, velocity=np.array([0.0, 0.0])):
        self._velocity = velocity
        super().__init__(figure=figure, position=position, color=color)

    def update_position(self):
        # x, y = obj.get_position()

        posx, posy = self.get_position()
        height, width = self.get_dimensions()

        posx += self._velocity[0]
        posy += self._velocity[1]

        if posx < 0:
            posx = 0

        if posx + width > config.WIDTH:
            posx = config.WIDTH - width

        if posy < 0:
            posy = 0

        if posy + height > config.HEIGHT:
            posy = config.HEIGHT - height

        self.set_position([posx, posy])

    def get_velocity(self):
        return self._velocity

    def set_velocity(self, velocity):
        self._velocity = velocity
