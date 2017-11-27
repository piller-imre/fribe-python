"""
Rule base class definition
"""


class RuleBase(object):
    """Represents a rule base."""

    def __init__(self, name=''):
        """
        Initialize a rule base with the given name.
        :param name: the unique name of the rule base
        """
        self._name = name
        self._description = ''
        self._universes = {}
        self._rules = []

    @property
    def name(self):
        return self._name

    def set_name(self, name):
        """
        Set the name of the rulebase.
        :param name: the new name of the universe
        :return: None
        """
        self._name = name

    @property
    def description(self):
        return self._description

    def set_description(self, description):
        """
        Set the description of the rulebase.
        :param description: the description of the rulebase
        :return: None
        """
        self._description = description

    def add_universe(self, name, universe):
        """
        Add new universe to the rule base.
        :param universe: a universe object
        :return: None
        """
        # WARN: Deprecated! Use add_universe method of the engine instead!
        if name in self._universes:
            raise ValueError('The universe "{}" has already added to the rulebase!'.format(name))
        self._universes[name] = universe

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
        for antecedent, expected_symbol in rule.predicates.items():
            if antecedent in self._universes:
                if antecedent in observation:
                    expected_value = self._universes[antecedent].get_term(expected_symbol).center
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
        distances = {symbol: [] for symbol in consequence_symbols}
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
        consequence = 0.0
        if self.has_zero_distance(distances):
            consequence = self.calc_matching_mean(distances)
        else:
            weight_sum = 0.0
            for symbol, distances in distances.items():
                value = self._universes[self._name].get_term(symbol).value
                for distance in distances:
                    weight = 1.0 / (distance ** 2)
                    consequence += value * weight
                    weight_sum += weight
            consequence /= weight_sum
        return consequence

    @staticmethod
    def has_zero_distance(distances):
        """
        Check that is there a zero distance in distance values.
        :param distances: {consequent symbol: [distances]} dictionary
        :return: True, when there is a zero value, else False
        """
        for value in distances.values():
            if 0.0 in value:
                return True
        return False

    def calc_matching_mean(self, distances):
        """
        Calculate the mean of the matching values.
        :param distances: {consequent symbol: [distances]} dictionary
        :return: the mean of the values where the distance is zero
        """
        s = 0.0
        n = 0
        for consequent, distance in distances.items():
            c = distance.count(0.0)
            if c > 0:
                s += c * self._universes[self._name].get_term(consequent).value
                n += c
        s /= n
        return s
