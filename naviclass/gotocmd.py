# -*- coding: utf-8 -*-

from bisect import bisect_left

import sublime
import sublime_plugin

from .util import LazyList, StatusMessage


FILTERS = {
    'source.python': lambda s: '(…)' not in s and '(' in s,
    None: lambda s: not s.startswith(' '),
}


class ClassNavigatorGoToClassCommand(sublime_plugin.TextCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status = StatusMessage(sublime_view=self.view)

    def run(self, edit):
        filter_func = FILTERS.get(self.syntax_name, FILTERS[None])

        items = [item for item in self.view.symbols() if filter_func(item[1])]

        self.status.clear()

        if items:
            self.locations, names = zip(*items)

            self.start_position = self.view.viewport_position()

            index = self.get_index_of_closest_region(
                self.current_line, self.locations)

            self.view.window().show_quick_panel(
                items=names,
                selected_index=index,
                on_select=self.jump_to,
                on_highlight=self.scroll_to,
            )
        else:
            self.status.show('ClassNavigator: no classes found')

    def get_index_of_closest_region(self, current_line, regions):
        """Get index of the item in `regions` which is closest to current
        location of cursor (or first selection block).
        """

        # convert regions to line numbers
        regions_lines = LazyList(
            regions,
            function=lambda r: self.view.rowcol(r.begin())[0],
        )

        # index of item which is >=
        index = bisect_left(regions_lines, current_line)

        if index == 0 or index == len(regions):
            return index

        a = regions_lines[index - 1]
        b = regions_lines[index]

        # find closest item among two
        if abs(current_line - a) < abs(current_line - b):
            return index - 1
        else:
            return index

    @property
    def current_line(self):
        selection = self.view.sel()
        if selection:
            return self.view.rowcol(selection[0].begin())[0]

        return 0

    @property
    def syntax_name(self):
        selection = self.view.sel()
        if selection:
            syntax_scope = self.view.scope_name(selection[0].begin())
            return syntax_scope.split(' ')[0]

    def scroll_to(self, index):
        """Scroll screen to selected item."""

        self.view.show_at_center(self.locations[index])

    def jump_to(self, index):
        """Jump to selected item: scroll screen and move cursor."""

        if index == -1:  # canceled
            self.view.set_viewport_position(self.start_position)
        else:
            position = sublime.Region(
                self.locations[index].begin(),
                self.locations[index].begin(),
            )
            self.view.sel().clear()
            self.view.sel().add(position)

            self.scroll_to(index)
