import numpy as np
import colorama as col
import random

import config
import graphics
import utils

from ball import Ball
from move_general import MoveGeneral


class PowerUp(MoveGeneral):
    def __init__(
        self,
        position=np.array([0.0, 0.0]),
        figure=np.array([[" "]]),
        type_power="",
        velocity=np.array([config.POWER_SPEED_X, config.POWER_SPEED_Y]),
    ):

        color = [[[config.POWER_BG_COL, config.POWER_COL]]]
        # velocity = np.array([config.POWER_SPEED_X, config.POWER_SPEED_Y])
        self._type = type_power
        self._frames = config.POWER_DUR
        self._start = False
        self._interval = 0
        super().__init__(
            figure=figure, position=position, color=color, velocity=velocity
        )

    def update_position(self):
        self._interval += 1
        posx, posy = self.get_position()
        height, width = self.get_dimensions()

        posx += self._velocity[0]
        if self._interval >= config.GRAVITY_INTERVAL:
            self._velocity[1] += config.GRAVITY
        # posy += self._velocity[1] + 1 / 2 * config.GRAVITY
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

    def get_type(self):
        return self._type

    def get_frames(self):
        return self._frames

    def reduce_frames(self):
        self._frames -= 1

    def get_start(self):
        return self._start

    def set_start(self):
        self._start = True

    def power(self, obj):
        pass

    def remove_power(self, obj):
        pass


class ExpandPaddle(PowerUp):
    def __init__(
        self,
        position=np.array([0.0, 0.0]),
        velocity=np.array([config.POWER_SPEED_X, config.POWER_SPEED_Y]),
    ):
        figure_string = graphics.EXPAND_PADDLE
        figure = utils.str_to_array(figure_string)

        super().__init__(
            figure=figure, position=position, type_power="e", velocity=velocity
        )

    def power(self, obj):
        unit = obj.get_figure_unit()
        height, width = obj.get_dimensions()
        if width >= config.PADDLE_LEN_MAX:
            return
        len = width + config.PADDLE_LEN_FACTOR
        len = min(len, config.PADDLE_LEN_MAX)
        figure = np.full((1, len), unit)
        obj.set_figure(figure)

    def remove_power(self, obj):
        unit = obj.get_figure_unit()
        height, width = obj.get_dimensions()
        if width <= config.PADDLE_LEN:
            return
        len = width - config.PADDLE_LEN_FACTOR
        len = max(len, config.PADDLE_LEN)
        figure = np.full((1, len), unit)
        obj.set_figure(figure)


class ShrinkPaddle(PowerUp):
    def __init__(
        self,
        position=np.array([0.0, 0.0]),
        velocity=np.array([config.POWER_SPEED_X, config.POWER_SPEED_Y]),
    ):
        figure_string = graphics.SHRINK_PADDLE
        figure = utils.str_to_array(figure_string)

        super().__init__(
            figure=figure, position=position, type_power="s", velocity=velocity
        )

    def power(self, obj):
        unit = obj.get_figure_unit()
        height, width = obj.get_dimensions()
        len = width - config.PADDLE_LEN_FACTOR
        len = max(len, config.PADDLE_LEN_MIN)
        figure = np.full((1, len), unit)
        obj.set_figure(figure)

    def remove_power(self, obj):
        unit = obj.get_figure_unit()
        height, width = obj.get_dimensions()
        len = width + config.PADDLE_LEN_FACTOR
        len = min(len, config.PADDLE_LEN)
        figure = np.full((1, len), unit)
        obj.set_figure(figure)


class BallMultiplier(PowerUp):
    def __init__(
        self,
        position=np.array([0.0, 0.0]),
        velocity=np.array([config.POWER_SPEED_X, config.POWER_SPEED_Y]),
    ):
        figure_string = graphics.BALL_MULTIPLIER
        figure = utils.str_to_array(figure_string)

        super().__init__(
            figure=figure, position=position, type_power="b", velocity=velocity
        )

    def power(self, obj):
        sign = lambda a: 1 if a > 0 else -1 if a < 0 else 0
        c_x, c_y = obj.get_position()
        v_x, v_y = obj.get_velocity()
        if np.array_equal(np.array([0.0, 0.0]), np.array([v_x, v_y])):
            new_ball = Ball(
                position=np.array([c_x, c_y]),
                velocity=np.array([config.BALL_SPEED_X, config.BALL_SPEED_Y]),
            )
        else:
            new_ball = Ball(
                position=np.array([c_x, c_y]),
                velocity=np.array([v_x + sign(v_x) * 0.3, v_y + sign(v_y) * 0.1]),
            )
        return new_ball


class FastBall(PowerUp):
    def __init__(
        self,
        position=np.array([0.0, 0.0]),
        velocity=np.array([config.POWER_SPEED_X, config.POWER_SPEED_Y]),
    ):
        figure_string = graphics.FAST_BALL
        figure = utils.str_to_array(figure_string)

        super().__init__(
            figure=figure, position=position, type_power="f", velocity=velocity
        )

    def power(self, obj):
        vx, vy = obj.get_velocity()
        vx = vx * config.BALL_DEC
        vy = vy * config.BALL_DEC

        obj.set_velocity([vx, vy])

    def remove_power(self, obj):
        vx, vy = obj.get_velocity()
        vx = vx / config.BALL_DEC
        vy = vy / config.BALL_DEC

        obj.set_velocity([vx, vy])


class ThruBall(PowerUp):
    def __init__(
        self,
        position=np.array([0.0, 0.0]),
        velocity=np.array([config.POWER_SPEED_X, config.POWER_SPEED_Y]),
    ):
        figure_string = graphics.THRU_BALL
        figure = utils.str_to_array(figure_string)

        super().__init__(
            figure=figure, position=position, type_power="t", velocity=velocity
        )

    def power(self, obj):
        color = [[[config.BALL_STRONG_BG_COL, config.BALL_COL]]]
        obj.set_color(color)
        obj.set_strong(True)

    def remove_power(self, obj):
        color = [[[config.BALL_BG_COL, config.BALL_COL]]]
        obj.set_color(color)
        obj.set_strong(False)


# class FireBall(PowerUp):
#     def __init__(
#         self,
#         position=np.array([0.0, 0.0]),
#         velocity=np.array([config.POWER_SPEED_X, config.POWER_SPEED_Y]),
#     ):
#         figure_string = graphics.FIRE_BALL
#         figure = utils.str_to_array(figure_string)

#         super().__init__(
#             figure=figure, position=position, type_power="fi", velocity=velocity
#         )

#     def power(self, obj):
#         color = [[[config.BALL_FIRE_BG_COL, config.BALL_COL]]]
#         obj.set_color(color)
#         obj.set_fire(True)

#     def remove_power(self, obj):
#         color = [[[config.BALL_BG_COL, config.BALL_COL]]]
#         obj.set_color(color)
#         obj.set_fire(False)


class PaddleGrab(PowerUp):
    def __init__(
        self,
        position=np.array([0.0, 0.0]),
        velocity=np.array([config.POWER_SPEED_X, config.POWER_SPEED_Y]),
    ):
        figure_string = graphics.PADDLE_GRAB
        figure = utils.str_to_array(figure_string)

        super().__init__(
            figure=figure, position=position, type_power="p", velocity=velocity
        )

    def power(self, obj):
        obj.set_sticky(True)

    def remove_power(self, obj):
        obj.set_sticky(False)


class PaddleShoot(PowerUp):
    def __init__(
        self,
        position=np.array([0.0, 0.0]),
        velocity=np.array([config.POWER_SPEED_X, config.POWER_SPEED_Y]),
    ):
        figure_string = graphics.PADDLE_SHOOT
        figure = utils.str_to_array(figure_string)

        super().__init__(
            figure=figure, position=position, type_power="ps", velocity=velocity
        )

    def power(self, obj):
        obj.set_figure_unit("^")
        height, width = obj.get_dimensions()
        figure = np.full((height, width), "^")
        obj.set_figure(figure)
        obj.set_shoot(True)

    def remove_power(self, obj):
        obj.set_figure_unit("=")
        height, width = obj.get_dimensions()
        figure = np.full((height, width), "=")
        obj.set_figure(figure)
        obj.set_shoot(False)


class Bullet(MoveGeneral):
    def __init__(self, position=np.array([0.0, 0.0])):

        color = [[[config.BULLET_BG_COL, config.BULLET_COL]]]
        velocity = np.array([config.BULLET_SPEED_X, config.BULLET_SPEED_Y])
        figure_string = graphics.BULLET
        figure = utils.str_to_array(figure_string)

        super().__init__(
            figure=figure, position=position, color=color, velocity=velocity
        )