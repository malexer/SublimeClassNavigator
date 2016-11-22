# Class Navigator

Class Navigator helps to quickly jump between classes and their methods in a
current file.


# Install

Install using Package Control:

1. Package Control: Install Package
2. Select by name `Class Navigator`


# Usage

## Go to Class

Show the list of classes in a current file and go to selected one.

* Command Palette -> Class Navigator: Go to Class

or

version | shortcut
---- | ----
Linux or Windows | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>C</kbd>
MacOS            | <kbd>⌘</kbd>+<kbd>Shift</kbd>+<kbd>C</kbd>


## Go to previous/next function

Jump to previous or next function/method in a current file.

* Command Palette -> Class Navigator: Go to previous Function
* Command Palette -> Class Navigator: Go to next Function

or

version | Go to previous | Go to next
---- | ----
Linux   | <kbd>Super</kbd>+<kbd>Alt</kbd>+<kbd>↑</kbd> | <kbd>Super</kbd>+<kbd>Alt</kbd>+<kbd>↓</kbd>
Windows | <kbd>Win</kbd>+<kbd>Alt</kbd>+<kbd>↑</kbd> | <kbd>Win</kbd>+<kbd>Alt</kbd>+<kbd>↓</kbd>
MacOS   | <kbd>⌘</kbd>+<kbd>Alt</kbd>+<kbd>↑</kbd> | <kbd>⌘</kbd>+<kbd>Alt</kbd>+<kbd>↓</kbd>


# Contributing

It is using "Goto Symbol..." under the hood with some additional filtering
defined in `naviclass.config`.

Currently class and method detection is tuned for Python source only.

For all other sources it is trying to detect first-level items for class and
consider all items in "Goto Symbol..." as methods.

Feel free to add more accurate class detection for other source types - check
the `naviclass/config.py`.
