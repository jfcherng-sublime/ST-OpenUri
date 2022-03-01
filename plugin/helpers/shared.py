from .utils import dotted_get
from .utils import dotted_set
from typing import Any, Dict, Optional, Pattern, Tuple
import logging
import sublime
import threading


class G:
    """This class stores application-level global variables."""

    # the plugin settings object
    settings: Optional[sublime.Settings] = None

    # the logger to log messages
    logger: Optional[logging.Logger] = None

    # the background thread for managing phantoms for views
    renderer_thread: Optional[threading.Thread] = None

    activated_schemes: Tuple[str, ...] = tuple()
    uri_regex_obj: Optional[Pattern[str]] = None

    images: Dict[str, Dict[str, Any]] = {
        # image informations
        # key/value structure is
        #     - "base64": "",
        #     - "bytes": b"",
        #     - "ext": "",
        #     - "mime": "",
        #     - "path": "",
        #     - "ratio_wh": 0,
        #     - "size": (0, 0),
        "phantom": {},
        "popup": {},
    }


def is_plugin_ready() -> bool:
    return bool(G.settings and G.uri_regex_obj)


def global_get(dotted: str, default: Optional[Any] = None) -> Any:
    return dotted_get(G, dotted, default)


def global_set(dotted: str, value: Any) -> None:
    return dotted_set(G, dotted, value)
