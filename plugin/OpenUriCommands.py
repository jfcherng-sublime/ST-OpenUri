from .helpers.functions import find_uri_regions_by_region
from .helpers.functions import find_uri_regions_by_regions
from .helpers.functions import open_uri_with_browser
from .helpers.settings import get_setting
import sublime
import sublime_plugin


class OpenUriFromCursorsCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit, browser: str = "") -> None:
        uris = map(
            self.view.substr,
            find_uri_regions_by_regions(self.view, self.view.sel(), get_setting("uri_search_radius")),
        )

        for uri in set(uris):
            open_uri_with_browser(uri, browser)


class OpenUriFromViewCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit, browser: str = "") -> None:
        region = (0, self.view.size())
        uris = map(
            self.view.substr,
            find_uri_regions_by_region(self.view, region, get_setting("uri_search_radius")),
        )

        for uri in set(uris):
            open_uri_with_browser(uri, browser)


class SelectUriFromCursorsCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit) -> None:
        sel = self.view.sel()

        if uri_regions := find_uri_regions_by_regions(self.view, sel, get_setting("uri_search_radius")):
            sel.clear()
            sel.add_all(uri_regions)


class SelectUriFromViewCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit) -> None:
        region = (0, self.view.size())
        sel = self.view.sel()

        if uri_regions := find_uri_regions_by_region(self.view, region, get_setting("uri_search_radius")):
            sel.clear()
            sel.add_all(uri_regions)
