import os
import sublime
from .plugin.functions import compile_uri_regex
from .plugin.Globals import global_get, global_set
from .plugin.log import apply_user_log_level, get_plugin_logger
from .plugin.settings import (
    get_image_info,
    get_package_name,
    get_settings_file,
    get_settings_object,
)

# main plugin classes
from .plugin.OpenUri import *
from .plugin.OpenUriCommands import *


def plugin_loaded() -> None:
    def plugin_settings_listener() -> None:
        apply_user_log_level(global_get("logger"))
        global_set("uri_regex_obj", compile_uri_regex())
        init_images()
        refresh_if_settings_file()

    def init_images() -> None:
        global_set("images.@cache", {})

        for img_name in global_get("images").keys():
            if img_name.startswith("@"):
                continue

            global_set("images.%s" % img_name, get_image_info(img_name))

    def refresh_if_settings_file() -> None:
        """ refresh the saved settings file to directly reflect visual changes """
        v = sublime.active_window().active_view()
        if os.path.basename(v.file_name() or "").endswith(get_settings_file()):
            v.run_command("revert")

    global_set("logger", get_plugin_logger())
    get_settings_object().add_on_change(get_package_name(), plugin_settings_listener)
    plugin_settings_listener()


def plugin_unloaded() -> None:
    get_settings_object().clear_on_change(get_package_name())
