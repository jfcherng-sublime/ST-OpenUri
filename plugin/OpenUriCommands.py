from .helpers.functions import find_uri_regions_by_regions
from .helpers.functions import open_uri_with_browser
from .helpers.settings import get_setting
from .helpers.types import EventDict, RegionLike, UriSource
from typing import Iterable, List, Optional
import sublime
import sublime_plugin


def get_uri_regions(
    view: sublime.View,
    source: UriSource,
    event: Optional[EventDict] = None,
) -> List[sublime.Region]:
    regions: Iterable[RegionLike]

    if source == UriSource.CONTEXT_MENU:
        regions = (view.window_to_text((event["x"], event["y"])),) * 2 if event else tuple()
    elif source == UriSource.CURSORS:
        regions = view.sel()
    elif source == UriSource.FILE:
        regions = ((0, view.size()),)
    else:
        raise RuntimeError
    return find_uri_regions_by_regions(view, regions, get_setting("uri_search_radius"))


class CopyUriFromContextMenuCommand(sublime_plugin.TextCommand):
    def description(self, event: EventDict) -> str:  # type: ignore
        return f"Copy {self._find_url(event)}"

    def is_visible(self, event: EventDict) -> bool:  # type: ignore
        return bool(self._find_url(event))

    def want_event(self) -> bool:
        return True

    def run(self, edit: sublime.Edit, event: EventDict) -> None:
        if url := self._find_url(event):
            sublime.set_clipboard(url)

    def _find_url(self, event: EventDict) -> str:
        uri_region = next(iter(get_uri_regions(self.view, UriSource.CONTEXT_MENU, event)), None)
        return self.view.substr(uri_region) if uri_region else ""


class OpenUriFromCursorsCommand(sublime_plugin.TextCommand):
    source = UriSource.CURSORS

    def run(self, edit: sublime.Edit, browser: str = "") -> None:
        for uri in set(map(self.view.substr, get_uri_regions(self.view, self.source))):
            open_uri_with_browser(uri, browser)


class OpenUriFromViewCommand(OpenUriFromCursorsCommand):
    source = UriSource.FILE


class SelectUriFromCursorsCommand(sublime_plugin.TextCommand):
    source = UriSource.CURSORS

    def run(self, edit: sublime.Edit) -> None:
        if uri_regions := get_uri_regions(self.view, self.source):
            sel = self.view.sel()
            sel.clear()
            sel.add_all(uri_regions)


class SelectUriFromViewCommand(SelectUriFromCursorsCommand):
    source = UriSource.FILE
