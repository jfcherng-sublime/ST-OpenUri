from .plugin import set_up, tear_down

# main plugin classes
from .plugin.sublime_text.OpenUri import *
from .plugin.sublime_text.OpenUriCommands import *

import sublime


def plugin_loaded() -> None:
    sublime.set_timeout_async(set_up)


def plugin_unloaded() -> None:
    tear_down()
