"""
Rule base class definition
"""


class RuleBase(object):
    """Represents a rule base."""

    def __init__(self, name):
        """
        Initialize a rule base with the given name.
        :param name: the unique name of the rule base
        """
        self._name = name
        self._universes = {}
        self._rules = []

    @property
    def name(self):
        return self._name

    def add_universe(self, universe):
        """
        Add new universe to the rule base.
        :param universe: a universe object
        :return: None
        """
        if universe.name in self._universes:
            raise ValueError('The universe "{}" has already added to the rulebase!'.format(universe.name))
        self._universes[universe.name] = universe

    def add_rule(self, rule):
        """
        Add new rule to the rule base.
        :param rule: a rule object
        :return: None
        """
        self._rules.append(rule)

    def calc_consequence(self, antecedent_values):
        """
        Calculate the consequence of the rule base.
        :param antecedent_values: the values of the antecedents as a dictionary
        :return: the calculated consequent value as a real number
        """
        pass
