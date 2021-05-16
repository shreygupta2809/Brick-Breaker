import numpy as np
import colorama as col
import random

import config
import graphics
import utils
from general import General


class Brick(General):
    def __init__(self, health=0, position=np.array([0.0, 0.0]), typeBrick="n"):

        self._health = health
        self._collisions = 0
        self._type = typeBrick

        config_bg_color = "BRICK_BG_COL_" + str(health)
        config_color = "BRICK_COL_" + str(health)

        color_bg_string = getattr(config, config_bg_color)
        color_string = getattr(config, config_color)

        color = [[[color_bg_string, color_string]]]

        figure_string = graphics.BRICK
        figure = utils.str_to_array(figure_string)

        super().__init__(figure=figure, position=position, color=color)

    def destroy(self, name, ball, explosion, brick_list):
        self._collisions += 1
        if name == "ball":
            if ball.get_strong() or explosion:
                self.set_active()
                if self._health < 4:
                    return self._health * 100, 1, []
                else:
                    return self._health * 100, 0, []
            
            # if ball.get_fire():
            #     self.set_active()
            #     score = 100
            #     count = 1
            #     brick_positions = []
            #     x, y = self.get_position()
            #     h, w = self.get_dimensions()
            #     for brik in brick_list:
            #         if brik.get_active():
            #             bx, by = brik.get_position()
            #             if (
            #                 (bx == x + w and y == by)
            #                 or (bx == x + w and y == by + h)
            #                 or (bx == x + w and y == by - h)
            #                 or (bx == x and y == by + h)
            #                 or (bx == x and y == by - h)
            #                 or (bx == x - w and y == by)
            #                 or (bx == x - w and y == by - h)
            #                 or (bx == x - w and y == by + h)
            #             ):
            #                 if brik.get_health() <= 4:
            #                     s, c, temp = brik.destroy(name, ball, True, brick_list)
            #                 else:
            #                     s, c, temp = brik.destroy(name, ball, brick_list)
            #                 score += s
            #                 count += c
            #                 brick_positions.append([bx, by])
            #                 brick_positions.extend(temp)

            #     return score, count, brick_positions

        if self._health == 4:
            return 0, 0, []
        self._health -= 1
        if self._health >= 1:
            config_bg_color = "BRICK_BG_COL_" + str(self._health)
            config_color = "BRICK_COL_" + str(self._health)

            color_bg_string = getattr(config, config_bg_color)
            color_string = getattr(config, config_color)

            color = [[[color_bg_string, color_string]]]
            self.set_color(color)
            return 100, 0, []
        else:
            self.set_active()
            return 100, 1, []

    def get_health(self):
        return self._health

    def set_health(self, health):
        self._health = health

    def get_num_collisions(self):
        return self._collisions

    def get_type(self):
        return self._type


class ExplodingBrick(Brick):
    def __init__(self, health=0, position=np.array([0.0, 0.0]), typeBrick="e"):

        super().__init__(position=position, health=health, typeBrick=typeBrick)

    def destroy(self, name, ball, brick_list):
        self.set_active()
        score = 100
        count = 1
        brick_positions = []
        x, y = self.get_position()
        h, w = self.get_dimensions()
        for brik in brick_list:
            if brik.get_active():
                bx, by = brik.get_position()
                if (
                    (bx == x + w and y == by)
                    or (bx == x + w and y == by + h)
                    or (bx == x + w and y == by - h)
                    or (bx == x and y == by + h)
                    or (bx == x and y == by - h)
                    or (bx == x - w and y == by)
                    or (bx == x - w and y == by - h)
                    or (bx == x - w and y == by + h)
                ):
                    if brik.get_health() <= 4:
                        s, c, temp = brik.destroy(name, ball, True, brick_list)
                    else:
                        s, c, temp = brik.destroy(name, ball, brick_list)
                    score += s
                    count += c
                    brick_positions.append([bx, by])
                    brick_positions.extend(temp)

        return score, count, brick_positions


class RainbowBrick(Brick):
    def __init__(self, health=0, position=np.array([0.0, 0.0]), typeBrick="r"):

        super().__init__(position=position, health=health, typeBrick=typeBrick)