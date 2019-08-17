import sublime
import sublime_plugin
from collections.abc import Iterable
from .functions import (
    find_uri_regions_by_region,
    open_uri_from_browser,
    view_last_update_timestamp_val,
    view_update_uri_regions,
    view_uri_regions_val,
)
from .Globals import Globals
from .settings import (
    get_colored_image_base64_by_region,
    get_package_name,
    get_setting,
    get_timestamp,
)

PHANTOM_TEMPLATE = """
    <body id="open-uri-phantom">
        <style>
            a {{
                line-height: 0;
            }}
            img {{
                width: {ratio_wh}em;
                height: 1em;
            }}
        </style>
        <a href="{uri}"><img src="data:{mime};base64,{base64}"></a>
    </body>
"""

POPUP_TEMPLATE = """
    <body id="open-uri-popup">
        <style>
            img {{
                width: {w}{size_unit};
                height: {h}{size_unit};
            }}
        </style>
        <a href="{uri}"><img src="data:{mime};base64,{base64}"></a>
        <span>Open this URI</span>
    </body>
"""


class OpenUriInBrowser(sublime_plugin.ViewEventListener):
    def __init__(self, view: sublime.View) -> None:
        self.view = view
        self.phantom_set = sublime.PhantomSet(self.view, get_package_name())
        view_last_update_timestamp_val(self.view, 0)
        view_uri_regions_val(self.view, [])

    def __del__(self) -> None:
        self._erase_phantom()
        self._erase_uri_regions()

    def on_load_async(self) -> None:
        if self._get_setting_show_open_button() != "always":
            self._erase_phantom()

        if self._get_setting_show_open_button() != "never" and self._clean_up_if_file_too_large():
            return

        self._detect_uris_globally()

    def on_activated_async(self) -> None:
        if self._get_setting_show_open_button() != "always":
            self._erase_phantom()

        if self._get_setting_show_open_button() != "never" and self._clean_up_if_file_too_large():
            return

        self._detect_uris_globally()

    def on_modified_async(self) -> None:
        if self._get_setting_show_open_button() != "never" and self._clean_up_if_file_too_large():
            return

        view_last_update_timestamp_val(self.view, get_timestamp())

        sublime.set_timeout_async(
            # fmt: off
            self.on_modified_async_callback,
            get_setting("on_modified_typing_period")
            # fmt: on
        )

    def on_modified_async_callback(self) -> None:
        now_s = get_timestamp()
        pass_ms = (now_s - view_last_update_timestamp_val(self.view)) * 1000

        if pass_ms >= get_setting("on_modified_typing_period"):
            view_last_update_timestamp_val(self.view, now_s)
            self._detect_uris_globally()

    def on_hover(self, point: int, hover_zone: int) -> None:
        if self._get_setting_show_open_button() == "hover":
            uri_regions = find_uri_regions_by_region(
                self.view, point, get_setting("uri_search_radius")
            )

            if hover_zone == sublime.HOVER_TEXT and uri_regions:
                self.view.show_popup(
                    self._generate_popup_html(uri_regions[0]),
                    flags=sublime.COOPERATE_WITH_AUTO_COMPLETE | sublime.HIDE_ON_MOUSE_MOVE_AWAY,
                    location=point,
                    max_width=500,
                    on_navigate=open_uri_from_browser,
                )

    def _detect_uris_globally(self) -> None:
        view_update_uri_regions(self.view, Globals.uri_regex_obj)

        uri_regions = [sublime.Region(*r) for r in view_uri_regions_val(self.view)]

        if self._get_setting_show_open_button() == "always":
            self._update_phantom(uri_regions)

        if get_setting("draw_uri_regions").get("enabled"):
            self._draw_uri_regions(uri_regions)
        else:
            self._erase_uri_regions()

    def _generate_phantom_html(self, uri_region: sublime.Region) -> str:
        # fmt: off
        return PHANTOM_TEMPLATE.format(
            uri=self.view.substr(uri_region),
            mime=Globals.image_phantom["mime"],
            ratio_wh=Globals.image_phantom["ratio_wh"],
            base64=get_colored_image_base64_by_region("phantom", uri_region),
        )
        # fmt: on

    def _generate_popup_html(self, uri_region: sublime.Region) -> str:
        base_size = 2.5

        # fmt: off
        return POPUP_TEMPLATE.format(
            uri=self.view.substr(uri_region),
            mime=Globals.image_popup["mime"],
            w=base_size * Globals.image_popup["ratio_wh"],
            h=base_size,
            size_unit="em",
            base64=get_colored_image_base64_by_region("popup", uri_region),
        )
        # fmt: on

    def _new_uri_phantom(self, uri_region: sublime.Region) -> sublime.Phantom:
        # Calculate the point to insert the phantom.
        #
        # Usually it's exact at the end of the URI, but if the next char is a quotation mark,
        # there can be a problem on breaking "scope brackets" highlighting in BracketHilighter.
        # In that case, we shift the position until the next char is not a quotation mark.
        phantom_point = uri_region.end()
        while self.view.substr(phantom_point) in "'\"`":
            phantom_point += 1

        return sublime.Phantom(
            sublime.Region(phantom_point),
            self._generate_phantom_html(uri_region),
            sublime.LAYOUT_INLINE,
            on_navigate=open_uri_from_browser,
        )

    def _new_uri_phantoms(self, uri_regions: Iterable) -> list:
        """
        @brief Note that "uri_regions" should be Iterable[sublime.Region]

        @return list[sublime.Phantom]
        """

        return [self._new_uri_phantom(r) for r in uri_regions]

    def _erase_phantom(self) -> None:
        self.phantom_set.update([])

    def _update_phantom(self, uri_regions: Iterable) -> None:
        """
        @brief Note that "uri_regions" should be Iterable[sublime.Region]
        """

        self.phantom_set.update(self._new_uri_phantoms(uri_regions))

    def _erase_uri_regions(self) -> None:
        self.view.erase_regions("OUIB_uri_regions")

    def _draw_uri_regions(self, uri_regions: Iterable) -> None:
        """
        @brief Note that "uri_regions" should be Iterable[sublime.Region]
        """

        draw_uri_regions = get_setting("draw_uri_regions")

        self.view.add_regions(
            "OUIB_uri_regions",
            list(uri_regions),
            scope=draw_uri_regions.get("scope"),
            icon=draw_uri_regions.get("icon"),
            flags=draw_uri_regions.get("flags"),
        )

    def _get_setting_show_open_button(self) -> str:
        return get_setting(
            "show_open_button_fallback" if self._is_file_too_large() else "show_open_button"
        )

    def _clean_up_if_file_too_large(self) -> bool:
        is_file_too_large = self._is_file_too_large()

        if is_file_too_large:
            view_uri_regions_val(self.view, [])
            self._erase_phantom()
            self._erase_uri_regions()

        return is_file_too_large

    def _is_file_too_large(self) -> bool:
        view_size = self.view.size()

        # somehow ST sometimes return size == 0 when reloading a file...
        # it looks like ST thinks the file content is empty during reloading
        # and triggered "on_modified_async()"
        if view_size == 0:
            return True

        return view_size > get_setting("use_show_open_button_fallback_if_file_larger_than")
