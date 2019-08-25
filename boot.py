from .plugin.functions import compile_uri_regex, set_is_dirty_for_all_views
from .plugin.Globals import global_get, global_set
from .plugin.log import apply_user_log_level, init_plugin_logger, log
from .plugin.RendererThread import RendererThread
from .plugin.settings import get_image_info, get_package_name, get_setting, get_settings_object

# main plugin classes
from .plugin.OpenUri import *
from .plugin.OpenUriCommands import *


def plugin_loaded() -> None:
    def plugin_settings_listener() -> None:
        apply_user_log_level(global_get("logger"))
        global_get("renderer_thread").set_interval(get_setting("renderer_interval"))

        uri_regex_obj, activated_schemes = compile_uri_regex()
        global_set("activated_schemes", activated_schemes)
        global_set("uri_regex_obj", uri_regex_obj)
        log("info", "Activated schemes: {}".format(activated_schemes))

        init_images()
        set_is_dirty_for_all_views(True)

    def init_images() -> None:
        global_set("images.@cache", {})

        for img_name in global_get("images").keys():
            if img_name.startswith("@"):
                continue

            global_set("images.%s" % img_name, get_image_info(img_name))

    global_set("logger", init_plugin_logger())
    global_set("renderer_thread", RendererThread())
    plugin_settings_listener()

    get_settings_object().add_on_change(get_package_name(), plugin_settings_listener)
    global_get("renderer_thread").start()


def plugin_unloaded() -> None:
    get_settings_object().clear_on_change(get_package_name())
    global_get("renderer_thread").cancel()
