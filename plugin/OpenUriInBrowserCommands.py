import sublime
import sublime_plugin
from .functions import (
    find_uri_regions_by_region,
    find_uri_regions_by_regions,
    open_uri_from_browser,
)
from .settings import get_setting


class SelectUriCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit) -> None:
        sel = self.view.sel()

        uri_regions = find_uri_regions_by_region(
            self.view, [0, self.view.size()], get_setting("uri_search_radius")
        )

        if uri_regions:
            sel.clear()
            sel.add_all(uri_regions)


class SelectUriFromCursorCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit) -> None:
        sel = self.view.sel()

        uri_regions = find_uri_regions_by_regions(self.view, sel, get_setting("uri_search_radius"))

        if uri_regions:
            sel.clear()
            sel.add_all(uri_regions)


class OpenUriInBrowserFromCursorCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit, browser="") -> None:
        uris = map(
            lambda region: self.view.substr(region),
            find_uri_regions_by_regions(
                self.view, self.view.sel(), get_setting("uri_search_radius")
            ),
        )

        for uri in set(uris):
            open_uri_from_browser(uri, browser)
