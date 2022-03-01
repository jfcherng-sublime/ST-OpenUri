from .helpers.functions import find_uri_regions_by_regions
from .helpers.functions import open_uri_with_browser
from .helpers.shared import is_plugin_ready
from .helpers.types import EventDict, RegionLike, UriSource
from abc import ABCMeta
from typing import Iterable, List, Optional
import sublime
import sublime_plugin


def get_uri_regions(view: sublime.View, source: UriSource, event: Optional[EventDict] = None) -> List[sublime.Region]:
    regions: Iterable[RegionLike]

    if source == UriSource.NONE:
        regions = tuple()
    elif source == UriSource.CONTEXT_MENU:
        regions = (view.window_to_text((event["x"], event["y"])),) * 2 if event else tuple()
    elif source == UriSource.CURSORS:
        regions = view.sel()
    elif source == UriSource.FILE:
        regions = ((0, view.size()),)
    else:
        raise RuntimeError
    return find_uri_regions_by_regions(view, regions)


class AbstractUriCommand(sublime_plugin.TextCommand, metaclass=ABCMeta):
    source = UriSource.NONE

    def is_enabled(self) -> bool:
        return is_plugin_ready()

    def is_visible(self) -> bool:
        return is_plugin_ready()

    def get_uri_regions(self, event: Optional[EventDict] = None) -> List[sublime.Region]:
        return get_uri_regions(self.view, self.source, event)


# -------- #
# copy URI #
# -------- #


class AbstractCopyUriCommand(AbstractUriCommand, metaclass=ABCMeta):
    def run(
        self,
        edit: sublime.Edit,
        event: Optional[EventDict] = None,
        unique: bool = True,
        sort: bool = True,
    ) -> None:
        if uri_regions := self.get_uri_regions(event):
            uris: Iterable[str] = map(self.view.substr, uri_regions)
            if unique:
                uris = set(uris)
            if sort:
                uris = sorted(uris)
            sublime.set_clipboard("\n".join(uris))


class CopyUriFromViewCommand(AbstractCopyUriCommand):
    source = UriSource.FILE


class CopyUriFromCursorsCommand(AbstractCopyUriCommand):
    source = UriSource.CURSORS


class CopyUriFromContextMenuCommand(AbstractCopyUriCommand):
    source = UriSource.CONTEXT_MENU

    def description(self, event: Optional[EventDict] = None) -> str:  # type: ignore
        return f"Copy {self._find_url(event)}"

    def is_visible(self, event: Optional[EventDict] = None) -> bool:  # type: ignore
        return super().is_visible() and bool(self.get_uri_regions(event))

    def want_event(self) -> bool:
        return True

    def _find_url(self, event: Optional[EventDict] = None) -> str:
        uri_region = next(iter(self.get_uri_regions(event)), None)
        return self.view.substr(uri_region) if uri_region else ""


# -------- #
# open URI #
# -------- #


class AbstractOpenUriCommand(AbstractUriCommand, metaclass=ABCMeta):
    def run(self, edit: sublime.Edit, event: Optional[EventDict] = None, browser: str = "") -> None:
        for uri in set(map(self.view.substr, self.get_uri_regions(event))):
            open_uri_with_browser(uri, browser)


class OpenUriFromViewCommand(AbstractOpenUriCommand):
    source = UriSource.FILE


class OpenUriFromCursorsCommand(AbstractOpenUriCommand):
    source = UriSource.CURSORS


# ---------- #
# select URI #
# ---------- #


class AbstractSelectUriCommand(AbstractUriCommand, metaclass=ABCMeta):
    def run(self, edit: sublime.Edit, event: Optional[EventDict] = None) -> None:
        if uri_regions := self.get_uri_regions(event):
            sel = self.view.sel()
            sel.clear()
            sel.add_all(uri_regions)


class SelectUriFromViewCommand(AbstractSelectUriCommand):
    source = UriSource.FILE


class SelectUriFromCursorsCommand(AbstractSelectUriCommand):
    source = UriSource.CURSORS
