"""
Engine class definition
"""


class Engine:
    """Represents the behavior engine."""

    def __init__(self):
        self._rulebases = {}

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

    def calc_consequences(self, antecedent_values):
        """
        Calculate the consequences of the available rule bases.
        :param antecedent_values: the values of the antecedents in a dictionary
        :return: the consequences in a dictionary with rule base names
        :raise ValueError: when there is an invalid antecedent name in the input dictionary
        """
        pass
