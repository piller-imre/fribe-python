import unittest

from fribe.universe import Universe
from fribe.term import Term


class UniverseTest(unittest.TestCase):
    """Test the Universe class"""

    def test_initialization(self):
        universe = Universe()
        self.assertEqual(universe.count_terms(), 0)

    def test_value_calculation_at_bounds(self):
        universe = Universe()
        a = Term('a', 0, 5)
        b = Term('b', 10, 8)
        universe.add_term(a)
        universe.add_term(b)
        a_value = universe.calc_value(0)
        self.assertEqual(a_value, 5)
        b_value = universe.calc_value(10)
        self.assertEqual(b_value, 8)

    def test_inner_value_calculation(self):
        universe = Universe()
        a = Term('a', 0, 5)
        b = Term('b', 10, 8)
        universe.add_term(a)
        universe.add_term(b)
        for x in range(11):
            value = universe.calc_value(x)
            reference = 5 + (x * 3) / 10
            self.assertEqual(value, reference)

    def test_simple_distance(self):
        universe = Universe()
        a = Term('a', 0, 5)
        b = Term('b', 10, 8)
        universe.add_term(a)
        universe.add_term(b)
        distance = universe.calc_distance(2, 7)
        self.assertEqual(distance, 0.5)
