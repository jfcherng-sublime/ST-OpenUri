from .plugin.functions import get_uri_regex_object
from .plugin.Globals import Globals
from .plugin.settings import get_image_info, get_package_name, get_settings_object

# main plugin classes
from .plugin.OpenUriInBrowser import *
from .plugin.OpenUriInBrowserCommands import *


def plugin_loaded() -> None:
    def plugin_settings_listener() -> None:
        Globals.uri_regex_obj = get_uri_regex_object()
        Globals.image_new_window = get_image_info("new_window")
        Globals.colored_image_base64 = {}

    get_settings_object().add_on_change(get_package_name(), plugin_settings_listener)
    plugin_settings_listener()


def plugin_unloaded() -> None:
    get_settings_object().clear_on_change(get_package_name())
