from ..functions import find_uri_regions_by_regions
from ..shared import is_plugin_ready
from ..types import EventDict, RegionLike
from abc import ABCMeta
from typing import Iterable, List, Optional
import enum
import sublime
import sublime_plugin


class UriSource(enum.Enum):
    CONTEXT_MENU = enum.auto()
    CURSORS = enum.auto()
    FILE = enum.auto()
    NONE = enum.auto()


class AbstractUriCommand(sublime_plugin.TextCommand, metaclass=ABCMeta):
    source = UriSource.NONE

    def is_enabled(self) -> bool:
        return is_plugin_ready()

    def is_visible(self) -> bool:
        return is_plugin_ready()

    def get_uri_regions(self, event: Optional[EventDict] = None) -> List[sublime.Region]:
        regions: Iterable[RegionLike]
        if self.source == UriSource.NONE:
            regions = tuple()
        elif self.source == UriSource.CONTEXT_MENU:
            if event:
                point = self.view.window_to_text((event["x"], event["y"]))
                regions = ((point, point),)
            else:
                regions = tuple()
        elif self.source == UriSource.CURSORS:
            regions = self.view.sel()
        elif self.source == UriSource.FILE:
            regions = ((0, self.view.size()),)
        else:
            raise RuntimeError
        return find_uri_regions_by_regions(self.view, regions)
