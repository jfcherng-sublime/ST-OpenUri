import sublime
from typing import Iterable, List
from .functions import open_uri_with_browser
from .Globals import global_get
from .image_processing import get_colored_image_base64_by_region
from .PhatomSetsManager import PhatomSetsManager
from .settings import get_package_name

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
    if not view:
        v_id = -1
        w_id = -1
    else:
        v_id = view.id()
        w = view.window()
        w_id = w.id() if w else -1

    return "w{w_id}v{v_id}".format(w_id=w_id, v_id=v_id)


def init_phantom_set(view: sublime.View) -> None:
    PhatomSetsManager.init_phantom_set(view, get_phantom_set_id(view), get_package_name())


def delete_phantom_set(view: sublime.View) -> None:
    PhatomSetsManager.delete_phantom_set(get_phantom_set_id(view))


def erase_phantom_set(view: sublime.View) -> None:
    PhatomSetsManager.erase_phantom_set(get_phantom_set_id(view))


def update_phantom_set(view: sublime.View, uri_regions: Iterable[sublime.Region]) -> None:
    PhatomSetsManager.update_phantom_set(
        get_phantom_set_id(view), new_uri_phantoms(view, uri_regions)
    )


def generate_phantom_html(view: sublime.View, uri_region: sublime.Region) -> str:
    img = global_get("images.phantom")

    return PHANTOM_TEMPLATE.format(
        uri=view.substr(uri_region),
        mime=img["mime"],
        ratio_wh=img["ratio_wh"],
        base64=get_colored_image_base64_by_region("phantom", uri_region),
    )


def new_uri_phantom(view: sublime.View, uri_region: sublime.Region) -> sublime.Phantom:
    # Calculate the point to insert the phantom.
    #
    # Usually it's exact at the end of the URI, but if the next char is a quotation mark,
    # there can be a problem on breaking "scope brackets" highlighting in BracketHilighter.
    # In that case, we shift the position until the next char is not a quotation mark.
    phantom_point = uri_region.end()
    while view.substr(phantom_point) in "'\"`":
        phantom_point += 1

    return sublime.Phantom(
        sublime.Region(phantom_point),
        generate_phantom_html(view, uri_region),
        layout=sublime.LAYOUT_INLINE,
        on_navigate=open_uri_with_browser,
    )


def new_uri_phantoms(
    view: sublime.View, uri_regions: Iterable[sublime.Region]
) -> List[sublime.Phantom]:

    return [new_uri_phantom(view, r) for r in uri_regions]
