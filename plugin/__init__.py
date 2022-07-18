import sublime

# import all listeners and commands
from .commands.copy_uri import CopyUriFromContextMenuCommand, CopyUriFromCursorsCommand, CopyUriFromViewCommand
from .commands.open_uri import OpenUriFromCursorsCommand, OpenUriFromViewCommand
from .commands.select_uri import SelectUriFromCursorsCommand, SelectUriFromViewCommand
from .constant import PLUGIN_NAME
from .functions import compile_uri_regex, view_is_dirty_val
from .listener import OpenUriViewEventListener
from .logger import apply_user_log_level, init_plugin_logger, log
from .phatom_sets_manager import PhatomSetsManager
from .renderer import RendererThread
from .settings import get_image_info, get_setting_renderer_interval, get_settings_object
from .shared import global_get, global_set
from .utils import is_processable_view

__all__ = (
    # ST: core
    "plugin_loaded",
    "plugin_unloaded",
    # ST: commands
    "CopyUriFromContextMenuCommand",
    "CopyUriFromCursorsCommand",
    "CopyUriFromViewCommand",
    "OpenUriFromCursorsCommand",
    "OpenUriFromViewCommand",
    "SelectUriFromCursorsCommand",
    "SelectUriFromViewCommand",
    # ST: listeners
    "OpenUriViewEventListener",
)


def plugin_loaded() -> None:
    sublime.set_timeout_async(plugin_loaded_real)


def plugin_loaded_real() -> None:
    global_set("settings", get_settings_object())
    global_set("logger", init_plugin_logger())
    global_set("renderer_thread", RendererThread())
    _settings_changed_callback()

    global_get("settings").add_on_change(PLUGIN_NAME, _settings_changed_callback)
    global_get("renderer_thread").start()


def plugin_unloaded() -> None:
    global_get("settings").clear_on_change(PLUGIN_NAME)
    global_get("renderer_thread").cancel()
    PhatomSetsManager.clear()


def _settings_changed_callback() -> None:
    apply_user_log_level(global_get("logger"))
    global_get("renderer_thread").set_interval(get_setting_renderer_interval())

    uri_regex_obj, activated_schemes = compile_uri_regex()
    global_set("activated_schemes", activated_schemes)
    global_set("uri_regex_obj", uri_regex_obj)
    log("info", f"Activated schemes: {activated_schemes}")

    _init_images()
    _set_is_dirty_for_all_views(True)


def _init_images() -> None:
    for img_name in global_get("images").keys():
        if not img_name.startswith("@"):
            global_set(f"images.{img_name}", get_image_info(img_name))


def _set_is_dirty_for_all_views(is_dirty: bool) -> None:
    """
    @brief Set is_dirty for all views.

    @param is_dirty Indicate if views are dirty
    """

    for w in sublime.windows():
        for v in w.views():
            if is_processable_view(v):
                view_is_dirty_val(v, is_dirty)
