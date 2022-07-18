import enum
from abc import ABC
from typing import Iterable, List, Optional

import sublime
import sublime_plugin

from ..functions import find_uri_regions_by_regions
from ..shared import is_plugin_ready
from ..types import EventDict, RegionLike


class UriSource(enum.Enum):
    CONTEXT_MENU = enum.auto()
    CURSORS = enum.auto()
    FILE = enum.auto()
    NONE = enum.auto()


class AbstractUriCommand(sublime_plugin.TextCommand, ABC):
    source = UriSource.NONE

    def is_enabled(self) -> bool:
        return is_plugin_ready()

    def is_visible(self) -> bool:
        return is_plugin_ready()

    def get_uri_regions(self, event: Optional[EventDict] = None) -> List[sublime.Region]:
        regions: Iterable[RegionLike] = tuple()
        if self.source == UriSource.NONE:
            pass
        elif self.source == UriSource.CONTEXT_MENU:
            if event:
                point = self.view.window_to_text((event["x"], event["y"]))
                regions = ((point, point),)
        elif self.source == UriSource.CURSORS:
            regions = self.view.sel()
        elif self.source == UriSource.FILE:
            regions = ((0, self.view.size()),)
        else:
            raise RuntimeError(f"Invalid UriSource type: {self.source}")
        return find_uri_regions_by_regions(self.view, regions)
