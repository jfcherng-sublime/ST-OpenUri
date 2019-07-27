import re
import sublime
import sublime_plugin
from .functions import (
    find_uri_regions_by_region,
    find_uri_regions_by_regions,
    open_uri_from_browser,
    view_find_all_fast,
    view_uri_regions_val,
)
from .settings import (
    # fmt: off
    get_image_path,
    get_setting,
    get_settings_object,
    get_uri_regex_by_schemes,
    # fmt: on
)

URI_REGEX = ""
URI_REGEX_OBJ = None


def plugin_loaded():
    settings_obj = get_settings_object()
    settings_obj.add_on_change("protocols", setting_protocols_refreshed)
    setting_protocols_refreshed()


def setting_protocols_refreshed():
    global URI_REGEX, URI_REGEX_OBJ

    URI_REGEX = get_uri_regex_by_schemes()
    URI_REGEX_OBJ = re.compile(URI_REGEX, re.IGNORECASE)


class OpenUriInBrowserFromCursorCommand(sublime_plugin.TextCommand):
    def run(self, edit, browser=""):
        uris = map(
            lambda region: self.view.substr(sublime.Region(*region)),
            find_uri_regions_by_regions(self.view, self.view.sel()),
        )

        for uri in set(uris):
            open_uri_from_browser(uri, browser)


class OpenUriInBrowser(sublime_plugin.ViewEventListener):
    def __init__(self, view):
        self.view = view
        self.phantom_set = sublime.PhantomSet(view)
        view_uri_regions_val(self.view, [])

    def on_load_async(self):
        self._detect_uris()

    def on_activated_async(self):
        self._detect_uris()

    def on_modified_async(self):
        self._detect_uris()

    def on_hover(self, point, hover_zone):
        if not get_setting("only_on_hover"):
            return

        self._update_phantom(find_uri_regions_by_region(self.view, point))

    def _detect_uris(self):
        uri_regions = view_find_all_fast(self.view, URI_REGEX_OBJ, False)

        # update found URi regions
        view_uri_regions_val(self.view, uri_regions)

        if get_setting("only_on_hover"):
            return

        self._update_phantom(uri_regions)

    def _generate_phantom_html(self, uri):
        view_font_size = self.view.settings().get("font_size")

        return '<a href="{uri}"><img width="{w}" height="{h}" src="res://{src}"></a>'.format(
            uri=uri, src=get_image_path(), w=view_font_size + 2, h=view_font_size + 2
        )

    def _new_uri_phantom(self, uri_region):
        # if the "uri_region" is tuple, list or...
        # always make "uri_region" a sublime.Region object
        if not isinstance(uri_region, sublime.Region):
            uri_region = sublime.Region(*(uri_region[0:2]))

        # calculate the point to insert the phantom usually it's exact at the end of URi, but if
        # the next char is a quotation mark, there could be a problem on break  "scope brackets"
        # highlighting in BracketHilighter. In that case, we shift the position until the next char
        # is not a quotation mark.
        phantom_point = uri_region.end()
        while self.view.substr(phantom_point) in "'\"":
            phantom_point += 1

        return sublime.Phantom(
            sublime.Region(phantom_point),
            self._generate_phantom_html(self.view.substr(uri_region)),
            sublime.LAYOUT_INLINE,
            on_navigate=open_uri_from_browser,
        )

    def _new_uri_phantoms(self, uri_regions):
        return [self._new_uri_phantom(r) for r in uri_regions]

    def _erase_phantom(self):
        self.phantom_set.update([])

    def _update_phantom(self, uri_regions):
        self.phantom_set.update(self._new_uri_phantoms(uri_regions))
