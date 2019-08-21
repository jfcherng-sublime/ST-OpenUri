import sublime
from .utils import dotted_get, dotted_set


class Globals:
    """
    @brief This class stores application-level global variables.
    """

    HAS_API_VIEW_STYLE_FOR_SCOPE = int(sublime.version()) >= 3170

    PHANTOM_TEMPLATE = """
    <body id="open-uri-phantom">
        <style>
            a {{
                line-height: 0;
            }}
            img {{
                width: {ratio_wh}em;
                height: 1em;
            }}
        </style>
        <a href="{uri}"><img src="data:{mime};base64,{base64}"></a>
    </body>
    """

    POPUP_TEMPLATE = """
    <body id="open-uri-popup">
        <style>
            img {{
                width: {w}{size_unit};
                height: {h}{size_unit};
            }}
        </style>
        <a href="{uri}"><img src="data:{mime};base64,{base64}"></a>
        <span>Open this URI</span>
    </body>
    """

    logger = None
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


def global_get(dotted: str, default=None):
    return dotted_get(Globals, dotted, default)


def global_set(dotted: str, value) -> None:
    return dotted_set(Globals, dotted, value)
