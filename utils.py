import numpy as np


def str_to_array(str):
    arr = str.split("\n")[1:-1]
    maxlen = len(max(arr, key=len))
    return np.array([list(x + (" " * (maxlen - len(x)))) for x in arr])


def clear_screen():
    print("\033[0;0H")
