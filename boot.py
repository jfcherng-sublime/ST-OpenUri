def plugin_reload() -> None:
    import sys

    prefix = f"{__package__}."
    for module_name in tuple(filter(lambda m: m.startswith(prefix) and m != __name__, sys.modules)):
        del sys.modules[module_name]


plugin_reload()

from .plugin import set_up
from .plugin import tear_down
from .plugin.commands import *  # noqa: F401, F403
from .plugin.listener import *  # noqa: F401, F403
import sublime


def plugin_loaded() -> None:
    sublime.set_timeout_async(set_up)


def plugin_unloaded() -> None:
    tear_down()
