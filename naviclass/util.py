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
