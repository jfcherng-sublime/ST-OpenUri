from .constant import PLUGIN_NAME
from .functions import compile_uri_regex
from .functions import view_is_dirty_val
from .logger import apply_user_log_level
from .logger import init_plugin_logger
from .logger import log
from .phatom_sets_manager import PhatomSetsManager
from .renderer import RendererThread
from .settings import get_image_info
from .settings import get_setting_renderer_interval
from .settings import get_settings_object
from .shared import global_get
from .shared import global_set
from .utils import is_processable_view
import sublime


def set_up() -> None:
    """plugin_loaded"""

    def plugin_settings_listener() -> None:
        apply_user_log_level(global_get("logger"))
        global_get("renderer_thread").set_interval(get_setting_renderer_interval())

        uri_regex_obj, activated_schemes = compile_uri_regex()
        global_set("activated_schemes", activated_schemes)
        global_set("uri_regex_obj", uri_regex_obj)
        log("info", f"Activated schemes: {activated_schemes}")

        init_images()
        set_is_dirty_for_all_views(True)

    global_set("settings", get_settings_object())
    global_set("logger", init_plugin_logger())
    global_set("renderer_thread", RendererThread())
    plugin_settings_listener()

    global_get("settings").add_on_change(PLUGIN_NAME, plugin_settings_listener)
    global_get("renderer_thread").start()


def tear_down() -> None:
    """plugin_unloaded"""

    global_get("settings").clear_on_change(PLUGIN_NAME)
    global_get("renderer_thread").cancel()
    PhatomSetsManager.clear()


def init_images() -> None:
    for img_name in global_get("images").keys():
        if not img_name.startswith("@"):
            global_set(f"images.{img_name}", get_image_info(img_name))


def set_is_dirty_for_all_views(is_dirty: bool) -> None:
    """
    @brief Set is_dirty for all views.

    @param is_dirty Indicate if views are dirty
    """

    for w in sublime.windows():
        for v in w.views():
            if is_processable_view(v):
                view_is_dirty_val(v, is_dirty)
