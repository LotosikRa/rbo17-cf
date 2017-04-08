""" This module contains algorithms. """
from settings import GOAL
from .logger import calc_lg


# helpers
def greatest_common_divisor(a, b):
    """ Euclid's algorithm """
    while b:
        a, b = b, a % b
    return a


# classes
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
            Chain(hand, self).add(self.hands[hand]).add(dot).register()
        else:
            self.hands[hand] = dot

    def register(self):
        for item in self.dots:
            if self.x == item.x and self.y == item.y:
                del self
        else:
            self.dots.append(self)

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
    goal = None
    approves = 0

    def __init__(self, hand, dot1):
        self.hand = hand
        self.dots = [dot1]
        self.len = 1
        self.approved = False

    def _add_dot(self, dot):
        if not dot in self.dots:
            self.dots.append(dot)
            return True
        else:
            return False

    def add(self, dot):
        if self._add_dot(dot):
            self.len += 1
            if self.len >= self.goal and not self.approved:
                self._approve()
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

    def _approve(self):
        Chain.approves = self.approves + 1
        self.approved = True

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


class Algorithm:

    def __init__(self):
        self.Chain = Chain
        self.Dot = Dot
        self.Hand = Hand

    def init_dots(self, array: list):
        for x, y in array:
            self.Dot(x, y).register()

    def init_hands(self):
        for dot in self.Dot.dots:
            dot.build_hands()

    def clear(self):
        self.Dot.dots = []
        self.Hand.hads = []
        self.Chain.chains = []
        self.Chain.approves = 0
        self.Chain.goal = 0

    def calculate(self, array, goal=GOAL):
        try:
            self.Chain.goal = goal
            self.init_dots(array)
            self.init_hands()
            points = self.get_points()
        except Exception as e:
            calc_lg.error(e)
            points = 'ERROR'
        else:
            calc_lg.info('Points - {} ; {}'.format(points, str(array)))
        finally:
            self.clear()
            return points

    def get_points(self):
        return self.Chain.approves


algo = Algorithm()
