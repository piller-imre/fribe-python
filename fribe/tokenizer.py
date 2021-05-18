from exprail import classifier
from exprail import parser
from exprail.token import Token


class CharClassifier(object):
    """Class for classifying the input characters"""

    @staticmethod
    def is_in_class(token_class, token):
        """
        Distinguish the input characters.
        :param token_class: ['0-9', 'a-Z', '"', '\\', '-', '.', 'empty']
        :param token: the considered token
        :return: True, when the token is in the given class, else False
        """
        if token.type == 'char':
            if token_class == '0-9':
                return token.value.isdigit()
            elif token_class == 'a-Z':
                return token.value.isalpha()
            elif token_class == '"':
                return token.value == '"'
            elif token_class == '\\':
                return token.value == '\\'
            elif token_class == '-':
                return token.value == '-'
            elif token_class == '.':
                return token.value == '.'
        elif token.type == 'empty':
            return token_class == 'empty'


class Tokenizer(parser.Parser):
    """Input character stream tokenizer class"""

    def __init__(self, grammar, source):
        super(Tokenizer, self).__init__(grammar, source)
        self._token = self.get_finish_token()

    def operate(self, operation, token):
        """
        Create a token with the given type.
        :param operation: ['keyword', 'text', 'number']
        :param token: the considered token (not the resulted)
        :return: None
        """
        if operation in ['keyword', 'text', 'number']:
            value = ''.join(self._stacks[''])
            self._token = Token(operation, value)
            self._ready = True
        else:
            raise ValueError('The operation name {} has not defined!'.format(operation))

    def get_finish_token(self):
        """Defines the empty token."""
        return Token('empty', '')

    def show_error(self, message, token):
        """Signs an error condition."""
        raise ValueError(message)
