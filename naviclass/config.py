from .util import Config


class DefaultConfig(object):
    """Default config which will be used for unsupported source."""

    def is_class(self, symbol_item):
        """Check if provided ``symbol_item`` is a name of the class."""
        return not symbol_item.startswith(' ')

    def is_function(self, symbol_item):
        """Check if provided ``symbol_item`` is a name of the function."""
        return True

    def index_of_function_name(self, line_str):
        """Return index of function name given the line string."""
        return 0


class PythonConfig(DefaultConfig):

    def is_class(self, symbol_item):
        """Check if provided ``symbol_item`` is a name of the class."""
        return '(…)' not in symbol_item and '(' in symbol_item

    def is_function(self, symbol_item):
        """Check if provided ``symbol_item`` is a name of the function."""
        return '(…)' in symbol_item

    def index_of_function_name(self, line_str):
        """Return index of function name given the line string."""
        if 'def ' in line_str:
            return line_str.index('def ') + 4

        return 0


config = Config({
    'source.python': PythonConfig(),
    None: DefaultConfig(),
})
