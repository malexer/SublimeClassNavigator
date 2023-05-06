from bisect import bisect_left

import sublime

from .util import LazyList


class Symbol(object):

    def __init__(self, name, region, sublime_view):
        self.name = name
        self.region = region
        self.sublime_view = sublime_view
        self._line_region = sublime_view.line(region)

    @property
    def line_number(self):
        """Return the line number of this symbol in the sublime_view."""
        return self.sublime_view.rowcol(self.region.begin())[0]

    @property
    def line_text(self):
        """Return this symbol line from sublime_view as a string."""
        return self.sublime_view.substr(self._line_region)

    def scroll(self):
        """Scroll view to this symbol."""
        self.sublime_view.show_at_center(self.region)

    def jump(self, cursor_offset=0):
        """Jump to this symbol: scroll view and move cursor."""

        start_location = self._line_region.begin() + cursor_offset
        position = sublime.Region(start_location, start_location)

        self.sublime_view.sel().clear()
        self.sublime_view.sel().add(position)

        self.scroll()


class SymbolList(object):

    def __init__(self, sublime_view, symbols=None):
        self.view = sublime_view

        if symbols is None:
            self.symbols = [
                Symbol(name=s[1], region=s[0], sublime_view=sublime_view)
                for s in self.view.symbols()  # list of tuples (Region, str)
            ]
        else:
            self.symbols = symbols

    def __getitem__(self, index):
        if index < 0:
            raise IndexError
        return self.symbols[index]

    def __len__(self):
        return len(self.symbols)

    @property
    def symbols(self):
        return self._symbols

    @symbols.setter
    def symbols(self, value):
        self._symbols = value
        # lazily calculate line number (locations) for each symbol
        # and cache calculated results
        self._line_nums = LazyList(
            value, function=lambda symbol: symbol.line_number)

    def is_symbol_on_line(self, line_number):
        """Check if there is any symbol on ``line_number``."""

        # index of item which is >=
        index = bisect_left(self._line_nums, line_number)

        if index >= len(self.symbols):
            return False
        return line_number == self._line_nums[index]

    def filter(self, func):
        """Filter symbols by function."""
        cls = type(self)
        return cls(
            sublime_view=self.view,
            symbols=[s for s in self.symbols if func(s)],
        )

    @property
    def names(self):
        """Get a list of names of symbols."""
        return [s.name for s in self.symbols]

    def closest_symbol_index(self, line_number):
        """Return the closest symbol index to given ``line_number``."""

        # index of item which is >=
        index = bisect_left(self._line_nums, line_number)

        if index == 0 or index == len(self):
            return index

        a = self._line_nums[index - 1]
        b = self._line_nums[index]

        # find closest item among two
        if abs(line_number - a) < abs(line_number - b):
            return index - 1
        else:
            return index

    def find_left(self, line_number):
        """Return the symbol which is just before the given ``line_number``."""

        # index of item which is >=
        index = bisect_left(self._line_nums, line_number)

        return self[index - 1]

    def find_right(self, line_number):
        """Return the symbol which is just after the ``line_number``."""

        # index of item which is >=
        index = bisect_left(self._line_nums, line_number)

        if self.is_symbol_on_line(line_number):
            return self[index + 1]
        else:
            return self[index]
