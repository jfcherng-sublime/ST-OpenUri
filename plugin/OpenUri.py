import sublime
import sublime_plugin
from .functions import (
    draw_uri_regions,
    find_uri_regions_by_region,
    generate_popup_html,
    open_uri_with_browser,
    view_is_dirty_val,
    view_last_typing_timestamp_val,
)
from .phantom_sets import init_phantom_set, delete_phantom_set
from .settings import get_setting, get_setting_show_open_button, get_timestamp


class OpenUri(sublime_plugin.ViewEventListener):
    def __init__(self, view: sublime.View) -> None:
        super().__init__(view)

        self.view = view
        init_phantom_set(self.view)
        view_is_dirty_val(self.view, True)
        view_last_typing_timestamp_val(self.view, 0)

    def on_pre_close(self) -> None:
        delete_phantom_set(self.view)

    def on_load_async(self) -> None:
        view_is_dirty_val(self.view, True)

    def on_modified_async(self) -> None:
        view_is_dirty_val(self.view, True)
        view_last_typing_timestamp_val(self.view, get_timestamp())

    def on_hover(self, point: int, hover_zone: int) -> None:
        if hover_zone != sublime.HOVER_TEXT:
            uri_regions = []
        else:
            uri_regions = find_uri_regions_by_region(
                self.view, point, get_setting("uri_search_radius")
            )

        if uri_regions and get_setting_show_open_button(self.view) == "hover":
            self.view.show_popup(
                generate_popup_html(self.view, uri_regions[0]),
                flags=sublime.COOPERATE_WITH_AUTO_COMPLETE | sublime.HIDE_ON_MOUSE_MOVE_AWAY,
                location=point,
                max_width=500,
                on_navigate=open_uri_with_browser,
            )

        if get_setting("draw_uri_regions.enabled") == "hover":
            draw_uri_regions(self.view, uri_regions)
