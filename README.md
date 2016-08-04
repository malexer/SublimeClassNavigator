# Class Navigator

Class Navigator helps to quickly go to class defenition in a current file.

It is using "Goto Symbol..." under the hood with some additional filtering.

Currently specific class detection is done for Python source only. All other
sources will be trying to detect first-level items.

Feel free to add more accurate class detection for other source types - check
the `FILTERS` dict in the `ClassNavigator.py`.


# Usage

version | shortcut
---- | ----
Linux or Windows | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>C</kbd>
MacOS            | <kbd>⌘</kbd>+<kbd>Shift</kbd>+<kbd>C</kbd>
