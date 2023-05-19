from __future__ import annotations

import sublime
import sublime_plugin

from .helpers import find_uri_regions_by_region
from .settings import get_setting, get_setting_show_open_button
from .ui.phantom_set import delete_phantom_set, init_phantom_set
from .ui.popup import show_popup
from .ui.region_drawing import draw_uri_regions
from .utils import get_timestamp, view_is_dirty_val, view_last_typing_timestamp_val


class OpenUriViewEventListener(sublime_plugin.ViewEventListener):
    def __init__(self, view: sublime.View) -> None:
        super().__init__(view)

        init_phantom_set(self.view)
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
            uri_regions: list[sublime.Region] = []
        else:
            uri_regions = find_uri_regions_by_region(self.view, point)

        if uri_regions and get_setting_show_open_button(self.view) == "hover":
            show_popup(self.view, uri_regions[0], point)

        if get_setting("draw_uri_regions.enabled") == "hover":
            draw_uri_regions(self.view, uri_regions)
