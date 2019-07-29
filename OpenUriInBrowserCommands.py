import sublime
import sublime_plugin
from .Globals import Globals
from .functions import find_uri_regions_by_regions, open_uri_from_browser, view_update_uri_regions


class SelectUriCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit) -> None:
        sel = self.view.sel()

        uri_regions = view_update_uri_regions(self.view, Globals.uri_regex_obj)

        if uri_regions:
            sel.clear()
            sel.add_all([sublime.Region(*r) for r in uri_regions])


class SelectUriFromCursorCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit) -> None:
        sel = self.view.sel()

        view_update_uri_regions(self.view, Globals.uri_regex_obj)
        uri_regions = find_uri_regions_by_regions(self.view, sel)

        if uri_regions:
            sel.clear()
            sel.add_all([sublime.Region(*r) for r in uri_regions])


class OpenUriInBrowserFromCursorCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit, browser="") -> None:
        uris = map(
            lambda region: self.view.substr(sublime.Region(*region)),
            find_uri_regions_by_regions(self.view, self.view.sel()),
        )

        for uri in set(uris):
            open_uri_from_browser(uri, browser)
