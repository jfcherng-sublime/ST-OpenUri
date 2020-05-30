import sublime
from .functions import compile_uri_regex, view_is_dirty_val
from .Globals import global_get, global_set
from .log import apply_user_log_level, init_plugin_logger, log
from .PhatomSetsManager import PhatomSetsManager
from .RendererThread import RendererThread
from .settings import (
    get_image_info,
    get_package_name,
    get_setting_renderer_interval,
    get_settings_object,
)
from .utils import is_view_normal_ready


def set_up() -> None:
    """ plugin_loaded """

    def plugin_settings_listener() -> None:
        apply_user_log_level(global_get("logger"))
        global_get("renderer_thread").set_interval(get_setting_renderer_interval())

        uri_regex_obj, activated_schemes = compile_uri_regex()
        global_set("activated_schemes", activated_schemes)
        global_set("uri_regex_obj", uri_regex_obj)
        log("info", "Activated schemes: {}".format(activated_schemes))

        init_images()
        set_is_dirty_for_all_views(True)

    global_set("logger", init_plugin_logger())
    global_set("renderer_thread", RendererThread())
    plugin_settings_listener()

    get_settings_object().add_on_change(get_package_name(), plugin_settings_listener)
    global_get("renderer_thread").start()


def tear_down() -> None:
    """ plugin_unloaded """

    get_settings_object().clear_on_change(get_package_name())
    global_get("renderer_thread").cancel()
    PhatomSetsManager.clear()


def init_images() -> None:
    global_set("images.@cache", {})

    for img_name in global_get("images").keys():
        if img_name.startswith("@"):
            continue

        global_set("images.%s" % img_name, get_image_info(img_name))


def set_is_dirty_for_all_views(is_dirty: bool) -> None:
    """
    @brief Set is_dirty for all views.

    @param is_dirty Indicate if views are dirty
    """

    for w in sublime.windows():
        for v in w.views():
            if is_view_normal_ready(v):
                view_is_dirty_val(v, is_dirty)
