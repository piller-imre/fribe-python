"""
Universe class definition
"""


class Universe(object):
    """Represents the universe of discourse."""

    def __init__(self):
        self._terms = {}

    def add_term(self, term):
        """
        Add new term to the universe.
        :param term: a term object
        :return: None
        :raise ValueError: when the term does not match with the existing terms
        """
        if term.name in self._terms:
            raise ValueError('The term "{}" has already exist in the universe!'.format(term.name))
        # TODO: Check the monotonity of the term values!
        self._terms[term.name] = term

    def calc_distance(self, a, b):
        """
        Calculate distance between two points on the universe.
        :param a: a real value
        :param b: a real value
        :return: distance as a real value
        :raise ValueError: when the a or the b is out of the domain of the universe
        """
        if a > b:
            a, b = b, a
        distance = self.calc_value(b) - self.calc_value(a)
        return distance

    def calc_value(self, x):
        """
        Calculate the value of the universe at the given point.
        :param x: a real value
        :return: the value of the universe as a real value
        :raise ValueError: when the x is out of the domain of the universe
        """
        term_centers = [term.center for term in self._terms]
        if x < min(term_centers):
            raise ValueError('The value {} is below the minimal domain value of the universe!'.format(x))
        if x > max(term_centers):
            raise ValueError('The value {} is above the maximal domain value of the universe!'.format(x))
        left_term = term_centers[0]
        right_term = term_centers[0]
        for term in term_centers:
            if x > term.center:
                if x - term.center < x - left_term.center:
                    left_term = term
            else:
                if term.center - x < right_term.center - x:
                    right_term = term
        ratio = (x - left_term.center) / (right_term.center - left_term.center)
        y = left_term.value + (right_term.value - left_term.value) * ratio
        return y

    def get_term(self, name):
        """
        Get the term by name.
        :param name: the name of the term
        :return: a term object
        """
        # TODO: Use ValueError instead of KeyError!
        return self._terms[name]
