"""
Rule class definition
"""


class Rule(object):
    """Represents a rule."""

    def __init__(self):
        self._predicates = {}
        self._consequent = None

    def add_predicate(self, antecedent_name, term_name):
        """
        Add new predicate to the rule.
        :param antecedent_name: the name of the antecedent
        :param term_name: the name of the term in the antecedent dimension
        :return: None
        :raise ValueError: when the predicate has already added to the rule
        """
        if antecedent_name in self._predicates:
            raise ValueError('The predicate "{}" has already added to the rule!'.format(antecedent_name))
        self._predicates[antecedent_name] = term_name

    @property
    def predicates(self):
        return self._predicates
