import logging
import threading
from typing import Any, Dict, Optional, Pattern, Tuple

import sublime

from .types import ImageDict
from .utils import dotted_get, dotted_set


class G:
    """This class stores application-level global variables."""

    settings: Optional[sublime.Settings] = None
    """the plugin settings object"""

    logger: Optional[logging.Logger] = None
    """the logger to log messages"""

    renderer_thread: Optional[threading.Thread] = None
    """the background thread for managing phantoms for views"""

    activated_schemes: Tuple[str, ...] = tuple()
    uri_regex_obj: Optional[Pattern[str]] = None

    images: Dict[str, ImageDict] = {
        "phantom": {},  # type: ignore
        "popup": {},  # type: ignore
    }


def is_plugin_ready() -> bool:
    return bool(G.settings and G.uri_regex_obj)


def global_get(dotted: str, default: Optional[Any] = None) -> Any:
    return dotted_get(G, dotted, default)


def global_set(dotted: str, value: Any) -> None:
    return dotted_set(G, dotted, value)
