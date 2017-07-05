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

    def collect_consequence_symbols(self):
        """
        Collect the consequence symbols of the rules.
        :return: the set of consequence symbol names.
        """
        consequence_symbols = set()
        for rule in self._rules:
            consequence_symbols.add(rule.consequent)
        return consequence_symbols

    def calc_distances_by_consequences(self, observation):
        """
        Calculate the rule distances grouped by consequence symbols.
        :return: a dictionary where the keys are the consequent symbols the values are the list of rule distances.
        """
        consequence_symbols = self.collect_consequence_symbols()
        distances = dict.fromkeys(consequence_symbols, [])
        for rule in self._rules:
            distances[rule.consequent].append(self.calc_distance(observation, rule))
        return distances

    def calc_consequence(self, observation):
        """
        Calculate the consequence of the rule base.
        :param observation: the values of the antecedents as a dictionary
        :return: the calculated consequent value as a real number
        """
        distances = self.calc_distances_by_consequences(observation)
        # TODO: Consider exact matches!
        weight_sum = 0.0
        consequence = 0.0
        for symbol, distances in distances.items():
            value = self._universes[self._name].get_term(symbol).value
            for distance in distances:
                weight = 1.0 / (distance ** 2)
                consequence += value * weight
                weight_sum += weight
        consequence /= weight_sum
        return consequence
