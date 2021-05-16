import numpy as np
import colorama as col


class General:
    def __init__(
        self,
        figure=np.array([[" "]]),
        position=np.array([0.0, 0.0]),
        color=np.array([[["", ""]]]),
    ):
        self._figure = figure
        self._position = position
        self._active = True

        self._height, self._width = self._figure.shape
        self._color = color

    def get_position(self):
        return self._position

    def set_position(self, position):
        self._position = position

    def get_color(self):
        return self._color

    def set_color(self, color):
        self._color = color

    def get_dimensions(self):
        return self._height, self._width

    def get_figure(self):
        return self._figure

    def set_figure(self, figure):
        self._figure = figure
        self._height, self._width = self._figure.shape

    def get_active(self):
        return self._active

    def set_active(self):
        self._active = False

    def get_velocity(self):
        return np.array([0.0, 0.0])