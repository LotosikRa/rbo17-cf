""" This module contains algorithms. """


# helpers
def greatest_common_divisor(a, b):
    """ Euclid's algorithm """
    while b:
        a, b = b, a % b
    return a


class Dot:
    """ Represents dots on the xOy (e.g. checkers on the field). """
    dots = []

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.register()

    def register(self):
        self.dots.append(self)


class Hand:
    """ Represents connections between Dots (e.g. lines between checkers). """
    hands = []

    def __init__(self, dot1, dot2):
        self.x, self.y = self.calculate_vector(dot1, dot2)
        self.register()

    def register(self):
        self.hands.append(self)

    @staticmethod
    def calculate_vector(dot1: Dot, dot2: Dot):
        x = abs(dot1.x - dot2.x)
        y = abs(dot1.y - dot2.y)
        gcd = greatest_common_divisor(x, y)
        return x/gcd, y/gcd


# steps
def init_dots(array):
    for x, y in array:
        Dot(x, y)


# main function
def calculate(x_long, y_long, total_dots, goal, input_array):
    """
    :param input_array: array with `y_long` arrays each one with `x_long` boolean integer (e.g. 0, 1)
    :param x_long: long of side A (x axis)
    :param y_long: long of side B (y axis)
    :param total_dots: number of checkers
    :param goal: minimum of checkers on the one line
    :return: points
    """
    init_dots(input_array)

    points = 0
    return points
