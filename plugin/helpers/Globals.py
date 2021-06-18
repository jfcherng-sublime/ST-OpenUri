from .utils import dotted_get
from .utils import dotted_set
from typing import Any, Dict, List, Optional, Pattern
import logging
import sublime
import threading


class Globals:
    """
    @brief This class stores application-level global variables.
    """

    HAS_API_VIEW_STYLE_FOR_SCOPE = int(sublime.version()) >= 3170

    # the plugin settings object
    settings = None  # type: sublime.Settings

    # the logger to log messages
    logger = None  # type: logging.Logger

    # the background thread for managing phantoms for views
    renderer_thread = None  # type: threading.Thread

    activated_schemes = []  # type: List[str]
    uri_regex_obj = None  # type: Pattern

    images = {
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
    }  # type: Dict[str, Any]


def global_get(dotted: str, default: Optional[Any] = None) -> Any:
    return dotted_get(Globals, dotted, default)


def global_set(dotted: str, value: Any) -> None:
    return dotted_set(Globals, dotted, value)
