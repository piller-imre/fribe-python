"""
Term class definition
"""


class Term(object):
    """Represents a term as a named symbol of the universe."""

    def __init__(self, name='', center=0.0, value=0.0):
        """
        Initialize the term object.
        :param name: the unique name of the term in the universe
        :param center: the center of the term on the domain
        :param value: the value of the term on the range
        """
        self._name = name
        self._center = center
        self._value = value

    @property
    def name(self):
        return self._name

    def set_name(self, name):
        """
        Set the name of the term.
        :param name: the name of the term
        :return: None
        """
        self._name = name

    @property
    def center(self):
        return self._center

    def set_center(self, center):
        """
        Set the center of the term.
        :param center: the center of the term
        :return: None
        """
        self._center = center

    @property
    def value(self):
        return self._value

    def set_value(self, value):
        """
        Set the value of the term.
        :param value: the value of the term
        :return: None
        """
        self._value = value
