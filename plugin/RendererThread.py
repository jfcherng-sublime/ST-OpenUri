import sublime
from .functions import (
    draw_uri_regions,
    erase_phantom_set,
    erase_uri_regions,
    is_view_normal_ready,
    is_view_too_large,
    is_view_typing,
    update_phantom_set,
    view_is_dirty_val,
)
from .Globals import global_get
from .log import log
from .RepeatingTimer import RepeatingTimer
from .settings import get_setting, get_setting_show_open_button
from .utils import view_find_all_fast


class RendererThread(RepeatingTimer):
    def __init__(self, interval_ms: int = 1000) -> None:
        super().__init__(interval_ms, self._check_current_view)

        # to prevent from overlapped processes when using a low interval
        self.is_job_running = False

    def _check_current_view(self) -> None:
        if self.is_job_running:
            return

        self.is_job_running = True

        view = sublime.active_window().active_view()

        if is_view_normal_ready(view) and is_view_too_large(view):
            self._clean_up_phantom_set(view)
            self._clean_up_uri_regions(view)
            view_is_dirty_val(view, False)

        if self._need_detect_chars_globally(view):
            self._detect_uris_globally(view)
            view_is_dirty_val(view, False)

        self.is_job_running = False

    def _need_detect_chars_globally(self, view: sublime.View) -> bool:
        return (
            is_view_normal_ready(view)
            and view_is_dirty_val(view)
            and not is_view_typing(view)
            and not is_view_too_large(view)
        )

    def _detect_uris_globally(self, view: sublime.View) -> None:
        uri_regions = view_find_all_fast(view, global_get("uri_regex_obj"), True)

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
