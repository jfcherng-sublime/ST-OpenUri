import re
import sublime
import sublime_plugin
from .functions import (
    find_uri_regions_by_region,
    open_uri_from_browser,
    view_typing_timestamp_val,
    view_update_uri_regions,
    view_uri_regions_val,
)
from .Globals import Globals
from .settings import (
    get_image_path,
    get_setting,
    get_settings_object,
    get_timestamp,
    get_uri_regex_by_schemes,
)


def plugin_loaded():
    def setting_detect_schemes_refreshed():
        Globals.uri_regex_obj = re.compile(get_uri_regex_by_schemes(), re.IGNORECASE)

    settings_obj = get_settings_object()
    settings_obj.add_on_change("detect_schemes", setting_detect_schemes_refreshed)
    setting_detect_schemes_refreshed()


class OpenUriInBrowser(sublime_plugin.ViewEventListener):
    def __init__(self, view):
        self.view = view
        self.phantom_set = sublime.PhantomSet(self.view)
        view_typing_timestamp_val(self.view, 0)
        view_uri_regions_val(self.view, [])

    def on_load_async(self):
        self._detect_uris()

    def on_activated_async(self):
        self._detect_uris()

    def on_modified_async(self):
        view_typing_timestamp_val(self.view, get_timestamp())

        sublime.set_timeout_async(
            # fmt: off
            self.on_modified_async_callback,
            get_setting("on_modified_typing_period")
            # fmt: on
        )

    def on_modified_async_callback(self):
        now_s = get_timestamp()
        pass_ms = (now_s - view_typing_timestamp_val(self.view)) * 1000

        if pass_ms >= get_setting("on_modified_typing_period"):
            view_typing_timestamp_val(self.view, now_s)
            self._detect_uris()

    def on_hover(self, point, hover_zone):
        if not get_setting("only_on_hover"):
            return

        self._update_phantom(find_uri_regions_by_region(self.view, point))

    def _detect_uris(self):
        uri_regions = view_update_uri_regions(self.view, Globals.uri_regex_obj)

        if get_setting("only_on_hover"):
            return

        self._update_phantom(uri_regions)

    def _generate_phantom_html(self, uri):
        view_font_size = self.view.settings().get("font_size")

        return '<a href="{uri}"><img width="{w}" height="{h}" src="res://{src}"></a>'.format(
            uri=uri, src=get_image_path(), w=view_font_size + 2, h=view_font_size + 2
        )

    def _new_uri_phantom(self, uri_region):
        # always make "uri_region" a sublime.Region object
        if not isinstance(uri_region, sublime.Region):
            uri_region = sublime.Region(*(uri_region[0:2]))

        # Calculate the point to insert the phantom.
        #
        # Usually it's exact at the end of URI, but if the next char is a quotation mark,
        # there could be a problem on break "scope brackets" highlighting in BracketHilighter.
        # In that case, we shift the position until the next char is not a quotation mark.
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
