import sublime
from typing import Iterable
from .settings import get_setting


def erase_uri_regions(view: sublime.View) -> None:
    view.erase_regions("OUIB_uri_regions")


def draw_uri_regions(view: sublime.View, uri_regions: Iterable[sublime.Region]) -> None:
    draw_uri_regions = get_setting("draw_uri_regions")

    view.add_regions(
        "OUIB_uri_regions",
        list(uri_regions),
        scope=draw_uri_regions["scope"],
        icon=draw_uri_regions["icon"],
        flags=draw_uri_regions["flags"],
    )
