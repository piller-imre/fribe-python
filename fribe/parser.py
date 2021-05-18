from exprail import classifier
from exprail import parser

from fribe.engine import Engine
from fribe.rule import Rule
from fribe.rulebase import RuleBase
from fribe.term import Term
from fribe.universe import Universe


class TokenClassifier(object):
    """Class for classifying the input tokens"""

    @staticmethod
    def is_in_class(token_class, token):
        """
        Distinguish the input tokens.
        :param token_class: ['keyword', 'text', 'number', ... keywords]
        :param token: the considered token
        :return: True, when the token is in the given class, else False
        """
        if token.type in ['text', 'number']:
            return token_class == token.type
        elif token.type == 'keyword':
            return token_class == token.value
        elif token.type == 'empty':
            return token_class == 'empty'
        else:
            raise ValueError('Unexpected token! ({}, {})'.format(token.type, token.value))


class Parser(parser.Parser):
    """Parser for the declarative behavior description"""

    def __init__(self, grammar, source):
        super(Parser, self).__init__(grammar, source)
        self._engine = Engine()
        self._universe = None
        self._term = None
        self._rulebase = None
        self._rule = None
        self._predicate = None

    @property
    def engine(self):
        return self._engine

    def operate(self, operation, token):
        """
        Apply the required operation.
        :param operation: one of the possible operation names
        :param token: the considered token
        :return: None
        """
        # print('# ' + operation + ' ({}, {})'.format(token.type, token.value))
        # TODO: Use a dedicated class for processing with the appropriate method names!
        if operation == 'create_universe':
            self._universe = Universe()
        elif operation == 'set_universe_name':
            self._universe.set_name(token.value)
        elif operation == 'set_universe_description':
            self._universe.set_description(token.value)
        elif operation == 'create_term':
            self._term = Term(token.value)
        elif operation == 'set_center':
            self._term.set_center(float(token.value))
        elif operation == 'set_value':
            self._term.set_value(float(token.value))
        elif operation == 'add_term':
            self._universe.add_term(self._term)
        elif operation == 'add_universe':
            self._engine.add_universe(self._universe)
        elif operation == 'create_rulebase':
            self._rulebase = RuleBase()
        elif operation == 'set_rulebase_name':
            self._rulebase.set_name(token.value)
        elif operation == 'set_rulebase_description':
            self._rulebase.set_description(token.value)
        elif operation == 'create_rule':
            self._rule = Rule()
        elif operation == 'set_rule_description':
            self._rule.set_description(token.value)
        elif operation == 'create_predicate':
            self._predicate = {'name': None, 'value': None}
        elif operation == 'set_consequence':
            self._rule.set_consequent(token.value)
        elif operation == 'set_predicate_name':
            self._predicate['name'] = token.value
        elif operation == 'set_predicate_value':
            self._predicate['value'] = token.value
        elif operation == 'add_predicate':
            self._rule.add_predicate(self._predicate['name'], self._predicate['value'])
        elif operation == 'add_rule':
            self._rulebase.add_rule(self._rule)
        elif operation == 'add_rulebase':
            self._engine.add_rulebase(self._rulebase)
        else:
            raise ValueError('The operation "{}" has not defined!'.format(operation))

    def show_error(self, message, token):
        """Signs an error condition."""
        raise ValueError('{} ({}, {})'.format(message, token.type, token.value))
