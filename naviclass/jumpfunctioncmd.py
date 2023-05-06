from .basecmd import ClassNavigatorBaseCmd
from .symbol import SymbolList


class ClassNavigatorJumpFunctionCommand(ClassNavigatorBaseCmd):

    def run(self, edit, jump_next=True):
        self.symbols = SymbolList(sublime_view=self.view) \
            .filter(func=self.syntax_config.is_function)

        self.status.clear()

        if self.symbols:
            try:
                if jump_next:
                    symbol = self.symbols.find_right(self.current_line)
                else:
                    symbol = self.symbols.find_left(self.current_line)
            except IndexError:
                # either trying to jump before first or after last function
                return

            # find the name of the function in string an jump to it
            func_name_index = self.syntax_config.index_of_function_name(symbol.line_text)
            symbol.jump(cursor_offset=func_name_index)
        else:
            self.status.show('ClassNavigator: no function(s) found')
