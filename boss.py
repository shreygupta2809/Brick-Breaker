import numpy as np
import colorama as col
import random

import config
import graphics
import utils

from move_general import MoveGeneral


class Boss(MoveGeneral):
    def __init__(self):

        color = [[[config.BOSS_BG_COL, config.BOSS_COL]]]

        figure_string = graphics.BOSS
        figure = utils.str_to_array(figure_string)
        h, w = figure.shape
        position = np.array([(config.WIDTH - w) // 2, 0])
        velocity = np.array([0.0, 0.0])

        self._health = 20
        self._def = 0

        super().__init__(
            figure=figure, position=position, color=color, velocity=velocity
        )

    def hit(self):
        if self._health > 1:
            self._health -= 1
        else:
            self._health -= 1
            self.set_active()

        return 100

    def get_health(self):
        return self._health

    def get_defense(self):
        return self._def
    
    def set_defense(self, value):
        self._def = value


class Bomb(MoveGeneral):
    def __init__(self, position=np.array([0.0, 0.0])):

        color = [[[config.BOMB_BG_COL, config.BOMB_COL]]]
        velocity = np.array([config.BOMB_SPEED_X, config.BOMB_SPEED_Y])
        figure_string = graphics.BOMB
        figure = utils.str_to_array(figure_string)

        super().__init__(
            figure=figure, position=position, color=color, velocity=velocity
        )