from __future__ import annotations

import logging
import threading
from typing import Any, Pattern

import sublime

from .types import ImageDict
from .utils import dotted_get, dotted_set


class G:
    """This class stores application-level global variables."""

    settings: sublime.Settings | None = None
    """the plugin settings object"""

    logger: logging.Logger | None = None
    """the logger to log messages"""

    renderer_thread: threading.Thread | None = None
    """the background thread for managing phantoms for views"""

    activated_schemes: tuple[str, ...] = tuple()
    uri_regex_obj: Pattern[str] | None = None

    images: dict[str, ImageDict] = {
        "phantom": {},  # type: ignore
        "popup": {},  # type: ignore
    }


def is_plugin_ready() -> bool:
    return bool(G.settings and G.uri_regex_obj)


def global_get(dotted: str, default: Any | None = None) -> Any:
    return dotted_get(G, dotted, default)


def global_set(dotted: str, value: Any) -> None:
    return dotted_set(G, dotted, value)
