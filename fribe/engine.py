"""
Engine class definition
"""


class Engine(object):
    """Represents the behavior engine."""

    def __init__(self):
        self._universes = {}
        self._rulebases = {}
        self._states = {}

    @property
    def universe_names(self):
        return list(self._universes.keys())

    @property
    def rulebase_names(self):
        return list(self._rulebase_names.keys())

    def add_universe(self, universe):
        """
        Add a new universe object to the engine.
        :param universe: a universe object
        :return: None
        :raise ValueError: when the universe has already exists in the engine
        """
        if universe.name in self._universes:
            raise ValueError('The universe "{}" has already added to the engine!'.format(universe.name))
        self._universes[universe.name] = universe

    def add_rulebase(self, rulebase):
        """
        Add a new rulebase object to the engine.
        :param rulebase: a rulebase object
        :return: None
        :raise ValueError: when the rulebase has already exists in the engine
        """
        if rulebase.name in self._rulebases:
            raise ValueError('The rulebase "{}" has already added to the engine!'.format(rulebase.name))
        self._rulebases[rulebase.name] = rulebase

    def set_state(self, name, value):
        """
        Set the given state value by name.
        :param name: the name of the input
        :param value: the float value of the input
        :return: None
        """
        self._states[name] = value

    def get_state(self, name):
        """
        Get the given state value by name
        :param name: the name of the input
        :return: the state value as a float
        """
        return self._states[name]

    def calc_consequences(self, observations):
        """
        Calculate the consequences of the available rule bases.
        :param observations: the values of the antecedents in a dictionary
        :return: the consequences in a dictionary with rule base names
        :raise ValueError: when there is an invalid antecedent name in the input dictionary
        """
        next_states = self._states.copy()
        for rulebase_name, rulebase in self._rulebases.items():
            next_states[rulebase_name] = rulebase.calc_consequence(self._universes, observations)
        self._states = next_states
