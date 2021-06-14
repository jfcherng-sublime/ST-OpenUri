from .settings import get_setting
from typing import Iterable, List, Union
import sublime


def erase_uri_regions(view: sublime.View) -> None:
    view.erase_regions("OUIB_uri_regions")


def draw_uri_regions(view: sublime.View, uri_regions: Iterable[sublime.Region]) -> None:
    draw_uri_regions = get_setting("draw_uri_regions")

    view.add_regions(
        "OUIB_uri_regions",
        list(uri_regions),
        scope=draw_uri_regions["scope"],
        icon=draw_uri_regions["icon"],
        flags=parse_draw_region_flags(draw_uri_regions["flags"]),
    )


def parse_draw_region_flags(flags: Union[int, List[str]]) -> int:
    # deprecated because it's not self-explanatory
    if isinstance(flags, int):
        return flags

    return sum(map(lambda flag: getattr(sublime, flag, 0), flags))
