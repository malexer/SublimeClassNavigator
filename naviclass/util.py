from bisect import bisect_left
import sys

import sublime


PY2 = sys.version_info.major == 2

if PY2:
    from UserDict import IterableUserDict as UserDict
    from UserList import UserList
else:
    from collections import UserDict, UserList


class LazyList(UserList):
    """List class with lazy access to items.

    Transformation ``function`` will be applied on access to the item.
    Result will be cached.
    """

    def __init__(self, source_list, function):
        self.data = source_list
        self.values = [None] * len(source_list)
        self.function = function

    def __getitem__(self, index):
        if self.values[index] is None:
            self.values[index] = self.function(self.data[index])

        return self.values[index]


class Config(UserDict):
    """Dict class returning value for key "None" as a default."""

    def __missing__(self, key):
        return self[None]


class RegionList(object):
    """Find regions by row number in sublime view (text buffer)."""

    def __init__(self, regions, sublime_view):
        self.regions = regions
        self.view = sublime_view

        # convert regions to line numbers
        self.region_lines = LazyList(
            regions, function=lambda r: self.view.rowcol(r.begin())[0])

    def has_region(self, line_number):
        """Check if there is any region located on the provided
        ``line_number``.
        """

        index = bisect_left(self.region_lines, line_number)
        if index >= len(self.region_lines):
            return False

        return line_number == self.region_lines[index]

    def prev_region_index(self, line_number):
        """Get index of the region which is located just before the
        ``line_number`` or they are both pointing to the same
        location (<=).
        """

        # index of item which is >=
        index = bisect_left(self.region_lines, line_number)

        if self.has_region(line_number):
            # "=="" case: line_number is pointing straight at the region
            return index
        else:
            return index - 1

    def closest_region_index(self, line_number):
        """Get index of the region which is closest to the
        ``line_number``.
        """

        # index of item which is >=
        index = bisect_left(self.region_lines, line_number)

        if index == 0 or index == len(self.regions):
            return index

        a = self.region_lines[index - 1]
        b = self.region_lines[index]

        # find closest item among two
        if abs(line_number - a) < abs(line_number - b):
            return index - 1
        else:
            return index


class StatusMessage(object):
    """Wrapper for Sublime Text status bar."""

    KEY = 'ClassNavigator'

    def __init__(self, sublime_view):
        self.view = sublime_view
        self.active = False

    def show(self, message):
        self.view.set_status(self.KEY, message)
        self.active = True

        sublime.set_timeout(self.clear, 5000)

    def clear(self):
        if self.active:
            self.view.erase_status(self.KEY)
            self.active = False
