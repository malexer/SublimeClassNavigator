import sys

import sublime


PY2 = sys.version_info.major == 2

if PY2:
    from UserList import UserList
else:
    from collections import UserList


class LazyList(UserList):
    """Lazily access item from list.

    Apply transformation function on access to the item.
    """

    def __init__(self, source_list, function):
        self.data = source_list
        self.function = function

    def __getitem__(self, key):
        return self.function(self.data[key])


class StatusMessage(object):

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
