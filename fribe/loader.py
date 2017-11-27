from exprail.grammar import Grammar
from exprail.source import SourceString

from fribe.tokenizer import CharClassifier
from fribe.tokenizer import Tokenizer
from fribe.parser import TokenClassifier
from fribe.parser import Parser


def load_engine_from_string(source):
    """
    Load the engine from string representation.
    :param source: the source text of the rulebase
    :return: an engine object
    """
    char_source = SourceString(source)
    char_classifier = CharClassifier()
    tokenizer_grammar = Grammar(filename='../grammars/simple/tokenizer.grammar', classifier=char_classifier)
    tokenizer = Tokenizer(tokenizer_grammar, char_source)
    token_classifier = TokenClassifier()
    parser_grammar = Grammar(filename='../grammars/simple/parser.grammar', classifier=token_classifier)
    parser = Parser(parser_grammar, tokenizer)
    parser.parse()
    return parser.engine
