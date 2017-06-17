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

    def calc_distance(self, observation, rule):
        """
        Calculate the distance of the observation from the given rule.
        :param observation: a dictionary with antecedent names and values
        :param rule: a rule object
        :raise ValueError: when the observation is invalid
        :return: a floating point value
        """
        predicate_distances = self.calc_predicate_distances(observation, rule)
        distance = sum([d ** 2 for d in predicate_distances]) / len(predicate_distances)
        # TODO: Normalize the value with the diagonal of the hypercube if necessary!
        return distance

    def calc_predicate_distances(self, observation, rule):
        """
        Calculate the distances of the predicates from the observation for the given rule.
        :param observation: a dictionary with antecedent names and values
        :param rule: a rule object
        :raise ValueError: when the observation is invalid
        :return: a list of floating point values
        """
        predicate_distances = []
        for antecedent, expected_value in rule.predicates.items():
            if antecedent in self._universes:
                if antecedent in observation:
                    universe = self._universes[antecedent]
                    value = observation[antecedent]
                    distance = universe.calc_distance(value, expected_value)
                    predicate_distances.append(distance)
                else:
                    raise ValueError('The {} antecedent is missing from the observation!'.format(antecedent))
            else:
                # TODO: It should be checked when the rule has added!
                raise ValueError('The universe is missing for the {}!'.format(antecedent))
        return predicate_distances

    def calc_consequence(self, antecedent_values):
        """
        Calculate the consequence of the rule base.
        :param antecedent_values: the values of the antecedents as a dictionary
        :return: the calculated consequent value as a real number
        """
        # TODO: Calculate the distances of the rules grouped by the consequences!
        pass
