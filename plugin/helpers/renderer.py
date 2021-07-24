from .functions import is_view_too_large
from .functions import is_view_typing
from .functions import view_is_dirty_val
from .log import log
from .phantom_set import erase_phantom_set
from .phantom_set import update_phantom_set
from .region_drawing import draw_uri_regions
from .region_drawing import erase_uri_regions
from .settings import get_setting
from .settings import get_setting_show_open_button
from .shared import global_get
from .timer import RepeatingTimer
from .utils import is_processable_view
from .utils import is_transient_view
from .utils import view_find_all_fast
from typing import Generator
import sublime


def foreground_views() -> Generator[sublime.View, None, None]:
    for window in sublime.windows():
        for group_idx in range(window.num_groups()):
            if view := window.active_view_in_group(group_idx):
                yield view


class RendererThread(RepeatingTimer):
    def __init__(self, interval_ms: int = 1000) -> None:
        super().__init__(interval_ms, self._update_foreground_views)

        # to prevent from overlapped processes when using a low interval
        self.is_rendering = False

    def _update_foreground_views(self) -> None:
        if self.is_rendering:
            return

        self.is_rendering = True
        for view in foreground_views():
            self._update_view(view)
        self.is_rendering = False

    def _update_view(self, view: sublime.View) -> None:
        if (
            not is_processable_view(view)
            or not view_is_dirty_val(view)
            or is_view_typing(view)
            or (is_transient_view(view) and not get_setting("work_for_transient_view"))
        ):
            return

        if is_view_too_large(view):
            self._clean_up_phantom_set(view)
            self._clean_up_uri_regions(view)
            view_is_dirty_val(view, False)
            return

        self._detect_uris_globally(view)
        view_is_dirty_val(view, False)

    def _detect_uris_globally(self, view: sublime.View) -> None:
        uri_regions = view_find_all_fast(view, global_get("uri_regex_obj"))

        # handle Phantoms
        if get_setting_show_open_button(view) == "always":
            update_phantom_set(view, uri_regions)
            log("debug_low", "re-render phantoms")
        else:
            self._clean_up_phantom_set(view)

        # handle draw URI regions
        if get_setting("draw_uri_regions.enabled") == "always":
            draw_uri_regions(view, uri_regions)
            log("debug_low", "draw URI regions")
        else:
            self._clean_up_uri_regions(view)

    def _clean_up_phantom_set(self, view: sublime.View) -> None:
        erase_phantom_set(view)
        log("debug_low", "erase phantoms")

    def _clean_up_uri_regions(self, view: sublime.View) -> None:
        erase_uri_regions(view)
        log("debug_low", "erase URI regions")