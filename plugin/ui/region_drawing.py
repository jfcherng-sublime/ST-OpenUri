from __future__ import annotations

from functools import reduce
from operator import xor
from typing import Iterable, Sequence

import sublime

from ..constants import URI_REGION_KEY
from ..settings import get_setting


def erase_uri_regions(view: sublime.View) -> None:
    view.erase_regions(URI_REGION_KEY)


def draw_uri_regions(view: sublime.View, uri_regions: Iterable[sublime.Region]) -> None:
    draw_uri_regions = get_setting("draw_uri_regions")

    view.add_regions(
        URI_REGION_KEY,
        tuple(uri_regions),
        scope=draw_uri_regions["scope"],
        icon=draw_uri_regions["icon"],
        flags=parse_draw_region_flags(draw_uri_regions["flags"]) | sublime.NO_UNDO,
    )


def parse_draw_region_flags(flags: int | Sequence[str]) -> int:
    if isinstance(flags, int):
        return flags

    return reduce(xor, map(lambda flag: getattr(sublime, flag, 0), flags), 0)
