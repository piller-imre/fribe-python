from exprail.grammar import Grammar
from exprail.source import SourceString

from fribe.tokenizer import CharClassifier
from fribe.tokenizer import Tokenizer
from fribe.parser import TokenClassifier
from fribe.parser import Parser

import os


def load_engine_from_string(source):
    """
    Load the engine from string representation.
    :param source: the source text of the rulebase
    :return: an engine object
    """
    package_directory = os.path.dirname(os.path.abspath(__file__))
    char_source = SourceString(source)
    char_classifier = CharClassifier
    tokenizer_path = os.path.join(package_directory, '../grammars/simple/tokenizer.grammar')
    tokenizer_grammar = Grammar(filename=tokenizer_path, classifier=char_classifier)
    tokenizer = Tokenizer(tokenizer_grammar, char_source)
    token_classifier = TokenClassifier
    parser_path = os.path.join(package_directory, '../grammars/simple/parser.grammar')
    parser_grammar = Grammar(filename=parser_path, classifier=token_classifier)
    parser = Parser(parser_grammar, tokenizer)
    parser.parse()
    return parser.engine

