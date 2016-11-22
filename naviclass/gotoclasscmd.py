# -*- coding: utf-8 -*-

import sublime
import sublime_plugin

from .config import config
from .util import RegionList, StatusMessage


class ClassNavigatorGoToClassCommand(sublime_plugin.TextCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status = StatusMessage(sublime_view=self.view)

    def run(self, edit):
        class_symbols = [
            item for item in self.view.symbols()
            if config[self.syntax_name].is_class(item[1])
        ]

        self.status.clear()

        if class_symbols:
            self.filtered_regions, class_names = zip(*class_symbols)

            regions = RegionList(self.filtered_regions, self.view)
            index = regions.closest_region_index(self.current_line)

            self.save_start_position()
            self.view.window().show_quick_panel(
                items=class_names,
                selected_index=index,
                on_select=self.jump_to,
                on_highlight=self.scroll_to,
            )
        else:
            self.status.show('ClassNavigator: no classes found')

    def save_start_position(self):
        self.start_position = self.view.viewport_position()

    def scroll_to(self, index):
        """Scroll screen to selected item."""

        self.view.show_at_center(self.filtered_regions[index])

    def jump_to(self, index, cursor_position=0):
        """Jump to selected item: scroll screen and move cursor.

        Cursor will be positioned to ``cursor_position`` char number
        in the line.
        """

        if index < 0 or index >= len(self.filtered_regions):
            self.view.set_viewport_position(self.start_position)
        else:
            position = sublime.Region(
                self.filtered_regions[index].begin() + cursor_position,
                self.filtered_regions[index].begin() + cursor_position,
            )
            self.view.sel().clear()
            self.view.sel().add(position)

            self.scroll_to(index)

    @property
    def current_line(self):
        """Get current line number."""

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
