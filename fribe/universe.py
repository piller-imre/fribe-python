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
        """
        pass
