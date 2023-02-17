from typing import Iterable, Tuple

import sublime

from ..constants import PLUGIN_NAME
from ..helpers import open_uri_with_browser
from ..shared import global_get
from ..types import ImageDict
from .image import get_colored_image_base64_by_region
from .phatom_sets_manager import PhatomSetsManager

PHANTOM_TEMPLATE = """
<body id="open-uri-phantom">
    <style>
        html, body {{
            margin: 0;
            padding: 0;
        }}
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


def get_phantom_set_id(view: sublime.View) -> str:
    return f"v{view.id()}"


def init_phantom_set(view: sublime.View) -> None:
    PhatomSetsManager.init_phantom_set(view, get_phantom_set_id(view), PLUGIN_NAME)


def delete_phantom_set(view: sublime.View) -> None:
    PhatomSetsManager.delete_phantom_set(get_phantom_set_id(view))


def erase_phantom_set(view: sublime.View) -> None:
    PhatomSetsManager.erase_phantom_set(get_phantom_set_id(view))


def update_phantom_set(view: sublime.View, uri_regions: Iterable[sublime.Region]) -> None:
    PhatomSetsManager.update_phantom_set(get_phantom_set_id(view), new_uri_phantoms(view, uri_regions))


def generate_phantom_html(view: sublime.View, uri_region: sublime.Region) -> str:
    img: ImageDict = global_get("images.phantom")

    return PHANTOM_TEMPLATE.format(
        uri=sublime.html_format_command(view.substr(uri_region)),
        mime=img["mime"],
        ratio_wh=img["ratio_wh"],
        base64=get_colored_image_base64_by_region("phantom", uri_region),
    )


def new_uri_phantom(view: sublime.View, uri_region: sublime.Region) -> sublime.Phantom:
    return sublime.Phantom(
        sublime.Region(uri_region.end()),
        generate_phantom_html(view, uri_region),
        layout=sublime.LAYOUT_INLINE,
        on_navigate=open_uri_with_browser,
    )


def new_uri_phantoms(view: sublime.View, uri_regions: Iterable[sublime.Region]) -> Tuple[sublime.Phantom, ...]:
    return tuple(new_uri_phantom(view, r) for r in uri_regions)
