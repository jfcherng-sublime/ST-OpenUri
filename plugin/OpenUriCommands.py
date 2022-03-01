from .helpers.functions import find_uri_regions_by_regions
from .helpers.functions import open_uri_with_browser
from .helpers.settings import get_setting
from .helpers.types import UriSource
from typing import List
import sublime
import sublime_plugin


def get_uri_regions(view: sublime.View, source: UriSource) -> List[sublime.Region]:
    if source == UriSource.CURSORS:
        regions = view.sel()
    elif source == UriSource.FILE:
        regions = ((0, view.size()),)
    else:
        raise RuntimeError
    return find_uri_regions_by_regions(view, regions, get_setting("uri_search_radius"))




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
