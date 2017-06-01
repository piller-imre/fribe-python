"""
Rule class definition
"""


class Rule(object):
    """Represents a rule"""

    def __init__(self):
        self._predicates = []
        self._consequent = None
