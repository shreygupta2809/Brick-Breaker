import numpy as np
import colorama as col
import random

import config
import graphics
import utils
from move_general import MoveGeneral


class Ball(MoveGeneral):
    def __init__(self, position=np.array([0.0, 0.0]), velocity=np.array([0.0, 0.0])):

        color = [[[config.BALL_BG_COL, config.BALL_COL]]]

        figure_string = graphics.BALL
        figure = utils.str_to_array(figure_string)

        self._strong = False
        # self._fire = False

        super().__init__(
            figure=figure, position=position, color=color, velocity=velocity
        )

    def get_strong(self):
        return self._strong

    def set_strong(self, value):
        self._strong = value

    # def get_fire(self):
    #     return self._fire

    # def set_fire(self, value):
    #     self._fire = value