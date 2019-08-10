import sublime
import sublime_plugin
from .functions import (
    find_uri_region_by_point,
    get_uri_regex_object,
    open_uri_from_browser,
    view_typing_timestamp_val,
    view_update_uri_regions,
    view_uri_regions_val,
)
from .Globals import Globals
from .settings import (
    get_image_info,
    get_package_name,
    get_setting,
    get_settings_object,
    get_timestamp,
)

PHANTOM_TEMPLATE = """
    <body id="open-uri-box">
        <style>
            a {{
                line-height: 0;
            }}
            img {{
                width: 1em;
                height: 1em;
            }}
        </style>
        <a href="{uri}"><img src="{data_uri}"></a>
    </body>
"""


def plugin_loaded() -> None:
    def plugin_settings_listener() -> None:
        Globals.uri_regex_obj = get_uri_regex_object()
        Globals.image_new_window = get_image_info("new_window")

    get_settings_object().add_on_change(get_package_name(), plugin_settings_listener)
    plugin_settings_listener()


def plugin_unloaded() -> None:
    get_settings_object().clear_on_change(get_package_name())


class OpenUriInBrowser(sublime_plugin.ViewEventListener):
    def __init__(self, view: sublime.View) -> None:
        self.view = view
        self.phantom_set = sublime.PhantomSet(self.view, get_package_name())
        view_typing_timestamp_val(self.view, 0)
        view_uri_regions_val(self.view, [])

    def __del__(self) -> None:
        self._erase_phantom()
        self._erase_uri_regions()

    def on_load_async(self) -> None:
        if self._clean_up_if_file_too_large():
            return

        self._detect_uris()

    def on_activated_async(self) -> None:
        if self._clean_up_if_file_too_large():
            return

        self._detect_uris()

    def on_modified_async(self) -> None:
        if self._clean_up_if_file_too_large():
            return

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
            uri_region = find_uri_region_by_point(self.view, point)
            self._update_phantom([uri_region] if uri_region else [])

    def _detect_uris(self) -> None:
        uri_regions = view_update_uri_regions(self.view, Globals.uri_regex_obj)

        if get_setting("show_open_button") == "always":
            self._update_phantom(uri_regions)

        if get_setting("draw_uri_regions").get("enabled"):
            self._draw_uri_regions(uri_regions)
        else:
            self._erase_uri_regions()

    def _generate_phantom_html(self, uri: str) -> None:
        return PHANTOM_TEMPLATE.format(uri=uri, **Globals.image_new_window)

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

    def _erase_uri_regions(self) -> None:
        self.view.erase_regions("OUIB_uri_regions")

    def _draw_uri_regions(self, uri_regions: list) -> None:
        settings = get_setting("draw_uri_regions")

        self.view.add_regions(
            "OUIB_uri_regions",
            [sublime.Region(*r) for r in uri_regions],
            scope=settings.get("scope"),
            icon=settings.get("icon"),
            flags=settings.get("flags"),
        )

    def _clean_up_if_file_too_large(self) -> bool:
        is_file_too_large = self._is_file_too_large()

        if is_file_too_large:
            view_uri_regions_val(self.view, [])
            self._erase_phantom()
            self._erase_uri_regions()

        return is_file_too_large

    def _is_file_too_large(self) -> bool:
        return self.view.size() > get_setting("disable_if_file_size_greater_than")
