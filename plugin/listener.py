from .functions import find_uri_regions_by_region
from .functions import view_is_dirty_val
from .functions import view_last_typing_timestamp_val
from .phantom_set import delete_phantom_set
from .phantom_set import init_phantom_set
from .popup import show_popup
from .region_drawing import draw_uri_regions
from .settings import get_setting
from .settings import get_setting_show_open_button
from .settings import get_timestamp
from typing import List
import sublime
import sublime_plugin


class OpenUri(sublime_plugin.ViewEventListener):
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
            uri_regions: List[sublime.Region] = []
        else:
            uri_regions = find_uri_regions_by_region(self.view, point)

        if uri_regions and get_setting_show_open_button(self.view) == "hover":
            show_popup(self.view, uri_regions[0], point)

        if get_setting("draw_uri_regions.enabled") == "hover":
            draw_uri_regions(self.view, uri_regions)
