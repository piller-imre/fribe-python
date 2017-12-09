"""
Universe class definition
"""


class Universe(object):
    """Represents the universe of discourse."""

    def __init__(self):
        # TODO: Inherit all class with name and description from the Block base class!
        self._name = ''
        self._description = ''
        self._terms = {}

    @property
    def name(self):
        return self._name

    def set_name(self, name):
        """
        Set the name of the universe.
        :param name: the name of the universe
        :return: None
        """
        self._name = name

    @property
    def description(self):
        return self._description

    def set_description(self, description):
        """
        Set the description of the universe.
        :param description: the description of the universe
        :return: None
        """
        self._description = description

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
        # NOTE: The normalization step is necessary!
        max_value = max([term.value for term in self._terms.values()])
        min_value = min([term.value for term in self._terms.values()])
        distance /= max_value - min_value
        return distance

    def calc_value(self, x):
        """
        Calculate the value of the universe at the given point.
        :param x: a real value
        :return: the value of the universe as a real value
        :raise ValueError: when the x is out of the domain of the universe
        """
        if not self.is_in_domain(x):
            raise ValueError('The value {} is out of the domain!'.format(x))
        left_term, right_term = self.find_neighbor_terms(x)
        y = self.interpolate(left_term.center, left_term.value, right_term.center, right_term.value, x)
        return y

    def find_neighbor_terms(self, x):
        """
        Find the neighbor terms of the given value.
        :param x: a real value
        :return: the two nearest terms at the left and right side of x
        """
        # TODO: Experimental bug fix. Create test cases!
        terms = sorted(self._terms.values(), key=lambda term: term.center)
        i = 0
        while i < len(terms):
            if terms[i].center == x:
                return terms[i], terms[i]
            elif terms[i].center < x < terms[i + 1].center:
                return terms[i], terms[i + 1]
            i += 1
        raise ValueError('The value {} is out of the domain!'.format(x))

    @staticmethod
    def interpolate(x0, y0, x1, y1, x):
        """
        Linear interpolation
        :return: the interpolated value
        """
        if x < x0 or x > x1:
            raise ValueError('The {} is not in range [{}, {}]!'.format(x, x0, x1))
        if x0 == x1:
            if y0 == y1:
                return y0
            else:
                raise ValueError('Invalid interpolation points!')
        ratio = (x - x0) / (x1 - x0)
        y = y0 + (y1 - y0) * ratio
        return y

    def get_term(self, name):
        """
        Get the term by name.
        :param name: the name of the term
        :return: a term object
        """
        if name in self._terms:
            return self._terms[name]
        else:
            raise ValueError('The term {} has not defined on the universe!'.format(name))

    def count_terms(self):
        """
        Count the terms of the universe.
        :return: the number of terms
        """
        return len(self._terms)

    def is_in_domain(self, x):
        """
        Check that the value is on the defined domain.
        :param x: a real value
        :return: True, when the x is in the domain, else False
        """
        centers = [term.center for term in self._terms.values()]
        return min(centers) <= x <= max(centers)
