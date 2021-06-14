from .plugin import set_up
from .plugin import tear_down
from .plugin.OpenUri import *
from .plugin.OpenUriCommands import *
import sublime


def plugin_loaded() -> None:
    sublime.set_timeout_async(set_up)


def plugin_unloaded() -> None:
    tear_down()
