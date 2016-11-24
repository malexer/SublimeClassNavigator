# -*- coding: utf-8 -*-

from .util import Config


class DefaultConfig(object):
    """Default config which will be used for unsupported source."""

    def is_class(self, symbol_item):
        """Check if provided ``symbol_item`` is a name of the class."""
        return not symbol_item.startswith(' ')

    def index_of_class_name(self, line_str):
        """Return index of class name given the line string."""
        return 0

    def is_function(self, symbol_item):
        """Check if provided ``symbol_item`` is a name of the function."""
        return True

    def index_of_function_name(self, line_str):
        """Return index of function name given the line string."""
        return 0


class PythonConfig(DefaultConfig):

    def _index_of_next_word(self, s, word):
        """Return the index of next word after ``word``."""
        parts = s.split()
        try:
            next_word = parts[parts.index(word) + 1]
            return s.index(next_word)
        except (IndexError, ValueError):
            return None

    def is_class(self, symbol_item):
        """Check if provided ``symbol_item`` is a name of the class."""
        return '(…)' not in symbol_item and '(' in symbol_item

    def index_of_class_name(self, line_str):
        """Return index of class name given the line string."""
        return self._index_of_next_word(line_str, word='class') or 0

    def is_function(self, symbol_item):
        """Check if provided ``symbol_item`` is a name of the function."""
        return '(…)' in symbol_item

    def index_of_function_name(self, line_str):
        """Return index of function name given the line string."""
        return self._index_of_next_word(line_str, word='def') or 0


config = Config({
    'source.python': PythonConfig(),
    None: DefaultConfig(),
})
