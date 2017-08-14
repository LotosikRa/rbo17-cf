""" This module contains algorithms.
Dot, Vector and Chain classes represents objects, while Algorithm
class provides just an interface for use.
See `Dot.build_vectors` and `Dot.check_connection` for understanding. """
from settings import GOAL
from .logger import calc_lg


# =================
# helpful-functions
# =================
def greatest_common_divisor(a, b):
    """ Euclid's algorithm """
    while b:
        a, b = b, a % b
    return a


def _check_type(obj, *expected) -> object:
    if type(obj) not in expected:
        raise RuntimeError(
            'Expected type: "{object_type}", got: "{expected_type}".'.format(
                object_type=type(obj), expected_type=expected))
    return obj


# =======
# Classes
# =======
class Dot:
    """ Represents dots on the xOy (e.g. checkers on the field). """

    dots = set()
    """ Field for storing all instantiated `Dot` objects. """
    build_all_lines = False

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.vectors = {}
        # to not use custom `register` method as for `Chain` and `Vector`
        self.dots.add(self)

    def __repr__(self):
        return '<Dot x:{} y:{}>'.format(self.x, self.y)

    def build_vectors(self):
        """ Builds vectors to all other dots (that are in `dots` field). """
        for dot in self.dots:
            if dot != self:  # if it is another dot
                vector = Vector(self, dot).register()  # add vector to storage
                self.check_connection(vector, dot)

    def check_connection(self, vector, dot):
        """ Checks if `self` have connection to this `dot` by this `vector`.
        If have, than creates new Chain, else store it in `vectors` dictionary.
        **Note**: this method is the most important """
        _check_type(vector, Vector)
        _check_type(dot, Dot)
        if vector in self.vectors:  # case when we have `dot` for this `vector`
            # create `Chain` object with 3 dots inside:
            # 1. `self`, 2. dot associated by `vector` 3. `dot`
            Chain(vector, self).add(self.vectors[vector]).add(dot).register()
        else:
            # add `dot` to the dictionary with `vector` as key, to
            # have access to this later
            self.vectors[vector] = dot
            if self.build_all_lines:
                Chain(vector, self).add(dot).register()


class Vector:
    """ Represents connections between Dots (e.g. lines between checkers). """

    vectors = set()
    """ Field for storing all vectors together. """

    def __init__(self, dot1: Dot, dot2: Dot):
        _check_type(dot1, Dot)
        _check_type(dot2, Dot)
        self.x, self.y = self.calculate_vector(dot1, dot2)

    def __repr__(self):
        return '<Vector x:{} y:{}>'.format(self.x, self.y)

    def __hash__(self):
        return id(self).__hash__()

    def __eq__(self, other):
        """ Compares vectors by their coordinates. Returns `True` if
        they ar collinear, else - `False` """
        return (self.x == other.x and self.y == other.y) or \
               (self.x == -other.x and self.y == -other.y)

    @staticmethod
    def calculate_vector(dot1: Dot, dot2: Dot) -> tuple:
        """ Returns pair of integers: x, y - coordinates of the vector
        between given dots. """
        _check_type(dot1, Dot)
        _check_type(dot2, Dot)
        x = dot1.x - dot2.x
        y = dot1.y - dot2.y
        gcd = greatest_common_divisor(max(x, y), min(x, y))
        return int(x/gcd), int(y/gcd)

    def register(self):
        """ Checks if it is equal vector in `vectors` field.
        If so - deletes `self`, else - appends `self` to `vectors`"""
        for item in self.vectors:
            if self == item:
                del self  # very dangerous place !!!
                return item
        else:
            self.vectors.add(self)
            return self


class Chain:
    """
    Represents groups of Dots connected with the same Vectors
    (e.g. checkers on one line).
    """

    chains = set()
    """ Field for storing all Chain objects. """

    def __init__(self, vector: Vector, dot1: Dot):
        _check_type(vector, Vector)
        _check_type(dot1, Dot)
        self.vector = vector
        self.dots = {dot1}

    @property
    def len(self):
        return len(self.dots)

    def __repr__(self):
        return '<Chain [Vector: {}, len: {}, dots: {}]>'\
            .format(self.vector, self.len, self.dots)

    def add(self, dot: Dot):
        """ If `dot` isn't in `dots` attribute (set) - append it and
        increment `len` attribute. """
        if dot not in self.dots:
            self.dots.add(dot)
        return self

    def _check_in(self, other):
        """ Checks if it is even one dot in both Chain objects.
        If so - return `True`, else - `False`. """
        _check_type(other, Chain)
        for dot in self.dots:
            if dot in other.dots:
                return True
        else:
            return False

    def _merge_in(self, other):
        """ Appends all dots that aren't in `other` to `other`. """
        _check_type(other, Chain)
        for dot in self.dots:
            if dot not in other.dots:
                other.add(dot)

    def register(self):
        """ Check if it is equivalent chain in `chains` field.
        Do comparing by calling `_check_in` method and comparing
        vectors, and if they are equal - call `merge_in` and
        deletes `self`, and returns `other`, else - return `self`. """
        for item in self.chains:
            if self.vector == item.vector and self._check_in(item):
                self._merge_in(item)
                del self
                return item
        else:
            self.chains.add(self)
            return self


class Algorithm:

    def __init__(self):
        self.Chain = Chain
        self.Dot = Dot
        self.Vector = Vector

    def init_dots(self, array: list):
        """ Initiate dots from coordinates in `array`."""
        for x, y in array:
            self.Dot(x, y)

    def init_vectors(self):
        """ Initiate Vectors by building connections from every dot. """
        for dot in self.Dot.dots:
            dot.build_vectors()

    def clear(self):
        """ Clear all initiated objects. """
        # this definition must remove all references to
        # created objects, so garbage collector must
        # delete them for ever
        self.Dot.dots = set()
        self.Vector.vectors = set()
        self.Chain.chains = set()

    def calculate(self, array: list or tuple, goal: int =GOAL, build_all_lines: bool =False, auto_correct: bool =True) -> int:
        """ Calculates how main points you have.
        Initiates all objects, counts points, logs result."""
        points = ''
        # checking input data
        _check_type(goal, int)
        _check_type(build_all_lines, bool)
        _check_type(auto_correct, bool)
        _check_type(array, list, tuple)
        if goal == 2 and not build_all_lines:
            if auto_correct:
                calc_lg.debug('Cannot calculate when "build_all_lines" is "False".')
                build_all_lines = True
                calc_lg.debug('Auto-correction performed: set "build_all_lines" to "True".')
            else:
                msg = 'Cannot calculate when "build_all_lines" is "False" and "goal" is "2".'
                calc_lg.error(msg)
                raise RuntimeError(msg)
        elif goal < 2:  # we cannot build Chain with less then 2 dots inside
            raise RuntimeError('Cannot calculate when "goal < 2".')
        elif build_all_lines:
            if auto_correct:
                calc_lg.debug('Overhead: "build_all_lines" will increase calculation time, setting it to "False".')
                build_all_lines = False
                calc_lg.debug('Auto-correction performed: set "build_all_lines" to "False".')
            else:
                calc_lg.debug('Overhead: "build_all_lines" will increase calculation time')
        else:
            calc_lg.debug('Starting calculation.')
        # actually calculation
        try:
            self.Dot.build_all_lines = build_all_lines
            self.init_dots(array)
            self.init_vectors()
            points = self._get_points(goal)
        except Exception as e:
            calc_lg.exception(e, exc_info=True)
            points = 'ERROR'
            raise e
        else:
            calc_lg.info('Points - {} ; {}'.format(points, str(array)))
        finally:
            self.clear()
            return points

    def _get_points(self, goal: int) -> int:
        """ Counts how many chains have more chan `goal` dots inside. """
        points = 0
        for chain in self.Chain.chains:
            if chain.len >= goal:
                points += 1
        return points


algo = Algorithm()
