import numpy as np
import colorama as col

import config
import utils
from general import General


class Paddle(General):
    def __init__(self):
        position = np.array(
            [int(config.WIDTH / 2 - config.PADDLE_LEN / 2), config.HEIGHT - 2]
        )
        self._fig_unit = "="
        self._sticky = False
        self._space = False
        self._shoot = False
        self._health = 5
        color = [[[config.PADDLE_BG_COL, config.PADDLE_COL]]]

        figure = np.full((1, config.PADDLE_LEN), self._fig_unit)

        super().__init__(figure=figure, position=position, color=color)

    def move(self, char, balls, boss):
        char = char.lower()

        posx, posy = self.get_position()
        height, width = self.get_dimensions()
        old_posx = posx

        if char == "a":
            posx -= config.PADDLE_SPEED
        elif char == "d":
            posx += config.PADDLE_SPEED

        if posx < 0:
            posx = 0

        if posx + width > config.WIDTH:
            posx = config.WIDTH - width

        if old_posx != posx and boss != None:
            boss_x, boss_y = boss.get_position()
            boss_h, boss_w = boss.get_dimensions()

            if char == "a":
                boss_x -= config.PADDLE_SPEED
            elif char == "d":
                boss_x += config.PADDLE_SPEED

            if boss_x < 0:
                boss_x = 0

            if boss_x + boss_w > config.WIDTH:
                boss_x = config.WIDTH - boss_w

            boss.set_position([boss_x, boss_y])

        if not (old_posx == posx):
            for ball in balls:
                if np.array_equal(ball.get_velocity(), np.array([0.0, 0.0])):
                    ball_x, ball_y = ball.get_position()
                    ball_h, ball_w = ball.get_dimensions()

                    if char == "a":
                        ball_x -= config.PADDLE_SPEED
                    elif char == "d":
                        ball_x += config.PADDLE_SPEED

                    if ball_x < 0:
                        ball_x = 0

                    if ball_x + ball_w > config.WIDTH:
                        ball_x = config.WIDTH - ball_w

                    ball.set_position([ball_x, ball_y])

        self.set_position([posx, posy])

    def get_figure_unit(self):
        return self._fig_unit

    def set_figure_unit(self, char):
        self._fig_unit = char

    def get_sticky(self):
        return self._sticky

    def set_sticky(self, value):
        self._sticky = value

    def get_space(self):
        return self._space

    def set_space(self, value):
        self._space = value

    def get_shoot(self):
        return self._shoot

    def set_shoot(self, value):
        self._shoot = value

    def get_health(self):
        return self._health

    def set_health(self):
        self._health -= 1