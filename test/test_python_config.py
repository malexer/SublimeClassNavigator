import unittest

from naviclass.config import PythonConfig


class IndexOfNextWordTestCase(unittest.TestCase):

    def setUp(self):
        self.func = PythonConfig()._index_of_next_word

    def test_first_word(self):
        self.assertEqual(self.func('some word', word='some'), 5)
        self.assertEqual(self.func('some word and', word='some'), 5)
        self.assertEqual(self.func('some  word and', word='some'), 6)
        self.assertEqual(self.func('some   word and another', word='some'), 7)

    def test_last_word(self):
        self.assertEqual(self.func('some word', word='word'), None)
        self.assertEqual(self.func('some word and', word='and'), None)

    def test_inside_word(self):
        self.assertEqual(self.func('some word and', word='word'), 10)
        self.assertEqual(self.func('some word  and another', word='word'), 11)

    def test_missing_word(self):
        self.assertEqual(self.func('some word and', word='missing'), None)

    def test_empty_word(self):
        self.assertEqual(self.func('some word and', word=''), None)

    def test_empty_string(self):
        self.assertEqual(self.func('', word='word'), None)

    def test_empty_word_and_string(self):
        self.assertEqual(self.func('', word=''), None)
