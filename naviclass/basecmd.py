import sublime_plugin

from .config import config
from .statusbar import StatusMessage


class ClassNavigatorBaseCmd(sublime_plugin.TextCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status = StatusMessage(sublime_view=self.view)

    def save_start_position(self):
        self.start_position = self.view.viewport_position()

    @property
    def current_line(self):
        """Get current line number."""

        selection = self.view.sel()
        if selection:
            return self.view.rowcol(selection[0].begin())[0]

        return 0

    @property
    def _syntax_name(self):
        """Get current syntax name."""
        selection = self.view.sel()
        if selection:
            syntax_scope = self.view.scope_name(selection[0].begin())
            return syntax_scope.split(' ')[0]

    @property
    def syntax_config(self):
        """Get current syntax config."""
        return config[self._syntax_name]
