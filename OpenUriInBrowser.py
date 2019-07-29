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
    get_package_name,
    get_setting,
    get_settings_object,
    get_timestamp,
    get_uri_regex_by_schemes,
)


def plugin_loaded() -> None:
    def setting_detect_schemes_refreshed() -> None:
        Globals.uri_regex_obj = re.compile(get_uri_regex_by_schemes(), re.IGNORECASE)

    settings_obj = get_settings_object()
    settings_obj.add_on_change("detect_schemes", setting_detect_schemes_refreshed)
    setting_detect_schemes_refreshed()


def plugin_unloaded() -> None:
    settings_obj = get_settings_object()
    settings_obj.clear_on_change("detect_schemes")


class OpenUriInBrowser(sublime_plugin.ViewEventListener):
    def __init__(self, view: sublime.View) -> None:
        self.view = view
        self.phantom_set = sublime.PhantomSet(self.view, get_package_name())
        view_typing_timestamp_val(self.view, 0)
        view_uri_regions_val(self.view, [])

    def __del__(self) -> None:
        self._erase_phantom()

    def on_load_async(self) -> None:
        self._detect_uris()

    def on_activated_async(self) -> None:
        self._detect_uris()

    def on_modified_async(self) -> None:
        view_typing_timestamp_val(self.view, get_timestamp())

        sublime.set_timeout_async(
            # fmt: off
            self.on_modified_async_callback,
            get_setting("on_modified_typing_period")
            # fmt: on
        )

    def on_modified_async_callback(self) -> None:
        now_s = get_timestamp()
        pass_ms = (now_s - view_typing_timestamp_val(self.view)) * 1000

        if pass_ms >= get_setting("on_modified_typing_period"):
            view_typing_timestamp_val(self.view, now_s)
            self._detect_uris()

    def on_hover(self, point: int, hover_zone: int) -> None:
        if get_setting("show_open_button") == "hover":
            self._update_phantom(find_uri_regions_by_region(self.view, point))

    def _detect_uris(self) -> None:
        uri_regions = view_update_uri_regions(self.view, Globals.uri_regex_obj)

        if get_setting("show_open_button") == "always":
            self._update_phantom(uri_regions)

    def _generate_phantom_html(self, uri: str) -> None:
        view_font_size = self.view.settings().get("font_size")

        return '<a href="{uri}"><img width="{w}" height="{h}" src="res://{src}"></a>'.format(
            uri=uri, src=get_image_path(), w=view_font_size + 2, h=view_font_size + 2
        )

    def _new_uri_phantom(self, uri_region) -> sublime.Phantom:
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

    def _new_uri_phantoms(self, uri_regions: list) -> list:
        return [self._new_uri_phantom(r) for r in uri_regions]

    def _erase_phantom(self) -> None:
        self.phantom_set.update([])

    def _update_phantom(self, uri_regions: list) -> None:
        self.phantom_set.update(self._new_uri_phantoms(uri_regions))
