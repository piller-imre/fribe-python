import unittest

from exprail.grammar import Grammar
from exprail.source import SourceString

from fribe.tokenizer import CharClassifier
from fribe.tokenizer import Tokenizer


class TokenizerTest(unittest.TestCase):
    """Tests for the description language tokenizer"""

    def test_empty_stream(self):
        char_classifier = CharClassifier
        grammar = Grammar(filename='grammars/simple/tokenizer.grammar', classifier=char_classifier)
        source = SourceString('')
        parser = Tokenizer(grammar, source)
        parser.parse()
        token = parser.get_token()
        self.assertEqual('empty', token.type)
        self.assertEqual('', token.value)

    def test_whitespace_only_stream(self):
        char_classifier = CharClassifier
        grammar = Grammar(filename='grammars/simple/tokenizer.grammar', classifier=char_classifier)
        source = SourceString('      ')
        parser = Tokenizer(grammar, source)
        parser.parse()
        token = parser.get_token()
        self.assertEqual('empty', token.type)
        self.assertEqual('', token.value)

    def test_single_keyword(self):
        char_classifier = CharClassifier
        grammar = Grammar(filename='grammars/simple/tokenizer.grammar', classifier=char_classifier)
        source = SourceString('universe')
        parser = Tokenizer(grammar, source)
        parser.parse()
        token = parser.get_token()
        self.assertEqual('keyword', token.type)
        self.assertEqual('universe', token.value)

    def test_single_keyword_with_padding(self):
        char_classifier = CharClassifier
        grammar = Grammar(filename='grammars/simple/tokenizer.grammar', classifier=char_classifier)
        source = SourceString('     universe     ')
        parser = Tokenizer(grammar, source)
        parser.parse()
        token = parser.get_token()
        self.assertEqual('keyword', token.type)
        self.assertEqual('universe', token.value)

    def test_multiple_keywords(self):
        char_classifier = CharClassifier
        grammar = Grammar(filename='grammars/simple/tokenizer.grammar', classifier=char_classifier)
        source = SourceString('universe description rule when and is end')
        parser = Tokenizer(grammar, source)
        keywords = ['universe', 'description', 'rule', 'when', 'and', 'is', 'end']
        while keywords:
            parser.parse()
            token = parser.get_token()
            self.assertEqual('keyword', token.type)
            self.assertEqual(keywords.pop(0), token.value)

    def test_single_text(self):
        char_classifier = CharClassifier
        grammar = Grammar(filename='grammars/simple/tokenizer.grammar', classifier=char_classifier)
        source = SourceString('"single text"')
        parser = Tokenizer(grammar, source)
        parser.parse()
        token = parser.get_token()
        self.assertEqual('text', token.type)
        self.assertEqual('single text', token.value)

    def test_multiple_texts(self):
        char_classifier = CharClassifier
        grammar = Grammar(filename='grammars/simple/tokenizer.grammar', classifier=char_classifier)
        source = SourceString('"first"  "second"\n\n"third"')
        parser = Tokenizer(grammar, source)
        texts = ['first', 'second', 'third']
        while texts:
            parser.parse()
            token = parser.get_token()
            self.assertEqual('text', token.type)
            self.assertEqual(texts.pop(0), token.value)

    def test_quoted_texts(self):
        char_classifier = CharClassifier
        grammar = Grammar(filename='grammars/simple/tokenizer.grammar', classifier=char_classifier)
        source = SourceString('"\\"first\\""  "sec\\\\ond"\n\n"th\\\\\\"\\\\rd"')
        parser = Tokenizer(grammar, source)
        texts = ['"first"', 'sec\\ond', 'th\\"\\rd']
        while texts:
            parser.parse()
            token = parser.get_token()
            self.assertEqual('text', token.type)
            self.assertEqual(texts.pop(0), token.value)

    def test_single_number(self):
        char_classifier = CharClassifier
        grammar = Grammar(filename='grammars/simple/tokenizer.grammar', classifier=char_classifier)
        source = SourceString('1234')
        parser = Tokenizer(grammar, source)
        parser.parse()
        token = parser.get_token()
        self.assertEqual('number', token.type)
        self.assertEqual('1234', token.value)

    def test_multiple_integers(self):
        char_classifier = CharClassifier
        grammar = Grammar(filename='grammars/simple/tokenizer.grammar', classifier=char_classifier)
        source = SourceString(' 12 34 \n    -567   \n\n-8\n \n')
        parser = Tokenizer(grammar, source)
        numbers = ['12', '34', '-567', '-8']
        while numbers:
            parser.parse()
            token = parser.get_token()
            self.assertEqual('number', token.type)
            self.assertEqual(numbers.pop(0), token.value)

    def test_multiple_floats(self):
        char_classifier = CharClassifier
        grammar = Grammar(filename='grammars/simple/tokenizer.grammar', classifier=char_classifier)
        source = SourceString('.101, 10.20,\n\n -8.9  -7.6  -.888')
        parser = Tokenizer(grammar, source)
        numbers = ['.101', '10.20', '-8.9', '-7.6', '-.888']
        while numbers:
            parser.parse()
            token = parser.get_token()
            self.assertEqual('number', token.type)
            self.assertEqual(numbers.pop(0), token.value)

    def test_finish_token(self):
        char_classifier = CharClassifier
        grammar = Grammar(filename='grammars/simple/tokenizer.grammar', classifier=char_classifier)
        source = SourceString('end')
        parser = Tokenizer(grammar, source)
        parser.parse()
        token = parser.get_token()
        self.assertEqual('keyword', token.type)
        self.assertEqual('end', token.value)
        parser.parse()
        token = parser.get_token()
        self.assertEqual('empty', token.type)
        self.assertEqual('', token.value)
