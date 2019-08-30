import sublime
from typing import Any, Optional
from .utils import dotted_get, dotted_set


class Globals:
    """
    @brief This class stores application-level global variables.
    """

    HAS_API_VIEW_STYLE_FOR_SCOPE = int(sublime.version()) >= 3170

    # the logger to log messages
    logger = None

    # the background thread for managing phantoms for views
    renderer_thread = None

    activated_schemes = []
    uri_regex_obj = None

    images = {
        "@cache": {
            # cached base64 string for colored images
            # "{img_name}@{rgba_color_code}": base64 encoded image resource,
        },
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


def global_get(dotted: str, default: Optional[Any] = None) -> Any:
    return dotted_get(Globals, dotted, default)


def global_set(dotted: str, value: Any) -> None:
    return dotted_set(Globals, dotted, value)
