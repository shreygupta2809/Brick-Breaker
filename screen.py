import numpy as np
import colorama as col
import sys
import math

import config
import utils


class Screen:
    def __init__(self):
        self.width = config.WIDTH
        self.height = config.HEIGHT
        self.display = np.full((self.height, self.width), " ")
        self.color = np.full((self.height, self.width, 2), "", dtype=object)
        self.clear()

    def clear(self):
        self.display[:] = " "
        self.color[:, :, 0] = config.BG_COL
        self.color[:, :, 1] = config.FG_COL

    def draw(self, obj):
        x, y = obj.get_position()
        h, w = obj.get_dimensions()
        v_x, v_y = obj.get_velocity()

        x = int(x)
        y = int(y)
        h = int(h)
        w = int(w)

        figure = obj.get_figure()
        color = obj.get_color()

        self.display[y : y + h, x : x + w] = figure

        self.color[y : y + h, x : x + w] = color

    def show(self):
        out = ""

        for i in range(self.height):
            for j in range(self.width):
                out += "".join(self.color[i][j]) + self.display[i][j]
            out += "\n"
        sys.stdout.write(out + col.Style.RESET_ALL)
