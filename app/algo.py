""" This module contains algorithms. """
from settings import ROWS, COLUMNS, CHECKERS, GOAL


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
        self.hands = {}

    def build_hands(self):
        for dot in self.dots:
            if dot != self:  # if it is another dot
                hand = Hand(self, dot).register()  # add hand to storage
                self.check_connection(hand, dot)

    def check_connection(self, hand, dot):
        """ Checks if self have connection to this dot by this hand"""
        if hand in self.hands:
            Chain(hand, self).register().add(self.hands[hand]).register().add(dot)
        else:
            self.hands[hand] = dot

    def register(self):
        for item in self.dots:
            if self.x == item.x and self.y == item.y:
                del self  # very dangerous place !!!
                return False
        else:
            self.dots.append(self)
            return True

    def __repr__(self):
        return '<Dot x:{} y:{}>'.format(self.x, self.y)


class Hand:
    """ Represents connections between Dots (e.g. lines between checkers). """
    hands = []

    def __init__(self, dot1, dot2):
        self.x, self.y = self.calculate_vector(dot1, dot2)

    @staticmethod
    def calculate_vector(dot1: Dot, dot2: Dot):
        x = dot1.x - dot2.x
        y = dot1.y - dot2.y
        if 0 in [x, y]:
            return x, y
        gcd = greatest_common_divisor(max(x,y), min(x, y))
        return int(x/gcd), int(y/gcd)

    def __hash__(self):
        return id(self).__hash__()

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y) or \
               (self.x == -other.x and self.y == -other.y)

    def __repr__(self):
        return '<Hand x:{} y:{}>'.format(self.x, self.y)

    def register(self):
        for item in self.hands:
            if self == item:
                del self  # very dangerous place !!!
                return item
        else:
            self.hands.append(self)
            return self


class Chain:
    """ Represents groups of Dots connected with the same Hands (e.g. checkers on one line). """
    chains = []

    def __init__(self, hand, dot1):
        self.hand = hand
        self.dots = [dot1]
        self.len = 1

    def _add_dot(self, dot):
        if not dot in self.dots:
            self.dots.append(dot)
            return True
        else:
            return False

    def add(self, dot):
        if self._add_dot(dot):
            self.len += 1
        return self

    def _check_in(self, other):
        for dot in self.dots:
            if dot in other.dots:
                return True
        else:
            return False

    def _merge_in(self, other):
        for dot in self.dots:
            if dot not in other.dots:
                other.add(dot)

    def register(self):
        for item in self.chains:
            if self.hand == item.hand and self._check_in(item):
                self._merge_in(item)
                del self
                return item
        else:
            self.chains.append(self)
            return self

    def __repr__(self):
        return '<Chain [Hand: {}, len: {}, first Dot: {}]>'.format(self.hand, self.len, self.dots[0])


# steps
def clear():
    Dot.dots = []
    Hand.hads = []
    Chain.chains = []


def init_dots(array: list):
    for x, y in array:
        Dot(x, y).register()


def init_hands():
    for dot in Dot.dots:
        dot.build_hands()


def search_goals(goal):
    points = 0
    for chain in Chain.chains:
        if chain.len >= goal:
            points += 1
    return points


# main function
def calculate(input_array, goal=GOAL, x_long=COLUMNS, y_long=ROWS, total_dots=CHECKERS):
    """
    :param input_array: array with `y_long` arrays each one with `x_long` boolean integer (e.g. 0, 1)
    :param x_long: long of side A (x axis)
    :param y_long: long of side B (y axis)
    :param total_dots: number of checkers
    :param goal: minimum of checkers on the one line
    :return: points
    """
    clear()
    init_dots(input_array)
    init_hands()
    points = search_goals(goal)
    return points
