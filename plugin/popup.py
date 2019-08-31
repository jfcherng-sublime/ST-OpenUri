import sublime
from .functions import open_uri_with_browser
from .Globals import global_get
from .image_processing import get_colored_image_base64_by_region
from .settings import get_setting

POPUP_TEMPLATE = """
<body id="open-uri-popup">
    <style>
        img {{
            width: {w}{size_unit};
            height: {h}{size_unit};
        }}
    </style>
    <a href="{uri}"><img src="data:{mime};base64,{base64}"></a>
    {text_html}
</body>
"""


def generate_popup_html(view: sublime.View, uri_region: sublime.Region) -> str:
    img = global_get("images.popup")
    base_size = 2.5

    return POPUP_TEMPLATE.format(
        uri=view.substr(uri_region),
        mime=img["mime"],
        w=base_size * img["ratio_wh"],
        h=base_size,
        size_unit="em",
        base64=get_colored_image_base64_by_region("popup", uri_region),
        text_html=get_setting("popup_text_html"),
    )


def show_popup(view: sublime.View, uri_region: sublime.Region, point: int) -> None:
    view.show_popup(
        generate_popup_html(view, uri_region),
        flags=sublime.COOPERATE_WITH_AUTO_COMPLETE | sublime.HIDE_ON_MOUSE_MOVE_AWAY,
        location=point,
        max_width=500,
        on_navigate=open_uri_with_browser,
    )
