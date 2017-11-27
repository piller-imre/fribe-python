"""
Rule class definition
"""


class Rule(object):
    """Represents a rule."""

    def __init__(self, predicates=None, consequent=None):
        self._description = ''
        if predicates is None:
            self._predicates = {}
        else:
            self._predicates = predicates
        self._consequent = consequent

    @property
    def description(self):
        return self._description

    def set_description(self, description):
        """
        Set the description of the rule.
        :param description: the description of the rule
        :return: None
        """
        self._description = description

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

    def set_consequent(self, consequent):
        """
        Set the consequent value of the rule.
        :param consequent: the consequent value as a string of term name
        :return: None
        """
        self._consequent = consequent

    @property
    def predicates(self):
        return self._predicates

    @property
    def consequent(self):
        return self._consequent
