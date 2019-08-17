from .plugin.functions import compile_uri_regex
from .plugin.Globals import Globals
from .plugin.settings import get_image_info, get_package_name, get_settings_object

# main plugin classes
from .plugin.OpenUriInBrowser import *
from .plugin.OpenUriInBrowserCommands import *


def plugin_loaded() -> None:
    def plugin_settings_listener() -> None:
        Globals.uri_regex_obj = compile_uri_regex()
        init_images()

    def init_images() -> None:
        Globals.images["@cache"] = {}

        for img_name in Globals.images.keys():
            if img_name.startswith("@"):
                continue

            Globals.images[img_name] = get_image_info(img_name)

    get_settings_object().add_on_change(get_package_name(), plugin_settings_listener)
    plugin_settings_listener()


def plugin_unloaded() -> None:
    get_settings_object().clear_on_change(get_package_name())
