# -*- coding: utf-8 -*-

from .basecmd import ClassNavigatorBaseCmd
from .config import config
from .symbol import SymbolList


class ClassNavigatorGoToClassCommand(ClassNavigatorBaseCmd):

    def run(self, edit):
        self.symbols = SymbolList(sublime_view=self.view) \
            .filter_by_name(func=config[self.syntax_name].is_class)

        self.status.clear()

        if self.symbols:
            start_index = self.symbols.closest_symbol_index(self.current_line)

            self.save_start_position()
            self.view.window().show_quick_panel(
                items=self.symbols.names,
                selected_index=start_index,
                on_select=self.jump_to,
                on_highlight=self.scroll_to,
            )
        else:
            self.status.show('ClassNavigator: no classes found')

    def scroll_to(self, index):
        """Scroll screen to selected item."""

        self.symbols[index].scroll()

    def jump_to(self, index):
        """Jump to selected item: scroll screen and move cursor."""

        if index < 0 or index >= len(self.symbols):
            self.view.set_viewport_position(self.start_position)
        else:
            self.symbols[index].jump()
