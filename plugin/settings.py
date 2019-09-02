import base64
import os
import sublime
import sys
import tempfile
import time
from typing import Any, Dict, Optional
from .utils import dotted_get
from .log import log


def get_package_name() -> str:
    """
    @brief Getsthe package name.

    @return The package name.
    """

    # __package__ will be "THE_PLUGIN_NAME.plugin" under this folder structure
    # anyway, the top module should always be the plugin name
    return __package__.partition(".")[0]


def get_package_path() -> str:
    """
    @brief Gets the package path.

    @return The package path.
    """

    return "Packages/" + get_package_name()


def get_expanding_variables(window: Optional[sublime.Window]) -> Dict[str, Any]:
    variables = {
        "home": os.path.expanduser("~"),
        "package_name": get_package_name(),
        "package_path": get_package_path(),
        "temp_dir": tempfile.gettempdir(),
    }

    if window:
        variables.update(window.extract_variables())

    return variables


def get_image_path(img_name: str) -> str:
    """
    @brief Get the image resource path from plugin settings.

    @param img_name The image name

    @return The image resource path.
    """

    img_path = get_setting("image_files")[img_name]

    # assert for potential dev code typos
    assert isinstance(img_path, str)

    return sublime.expand_variables(img_path, get_expanding_variables(sublime.active_window()))


def get_image_info(img_name: str) -> Dict[str, Any]:
    """
    @brief Get image informations of an image from plugin settings.

    @param img_name The image name

    @return The image information.
    """

    from .libs import imagesize

    img_path = get_image_path(img_name)
    img_ext = os.path.splitext(img_path)[1]
    img_mime = "image/png"

    assert img_ext.lower() == ".png"

    try:
        img_bytes = sublime.load_binary_resource(img_path)
    except IOError:
        log("error", "Resource not found: " + img_path)

    img_base64 = base64.b64encode(img_bytes).decode()
    img_w, img_h = imagesize.get_from_bytes(img_bytes)

    return {
        "base64": img_base64,
        "bytes": img_bytes,
        "ext": img_ext,
        "mime": img_mime,
        "path": img_path,
        "ratio_wh": img_w / img_h,
        "size": (img_w, img_h),
    }


def get_image_color(img_name: str, region: sublime.Region) -> str:
    """
    @brief Get the image color from plugin settings in the form of #RRGGBBAA.

    @param img_name The image name
    @param region   The region

    @return The color code in the form of #RRGGBBAA
    """

    from .image_processing import color_code_to_rgba

    img_color = get_setting("image_colors")[img_name]

    # assert for potential dev code typos
    assert isinstance(img_color, str)

    return color_code_to_rgba(img_color, region)


def get_settings_file() -> str:
    """
    @brief Get the settings file name.

    @return The settings file name.
    """

    return get_package_name() + ".sublime-settings"


def get_settings_object() -> sublime.Settings:
    """
    @brief Get the plugin settings object.

    @return The settings object.
    """

    return sublime.load_settings(get_settings_file())


def get_setting(dotted: str, default: Optional[Any] = None) -> Any:
    """
    @brief Get the plugin setting with the dotted key.

    @param dotted  The dotted key
    @param default The default value if the key doesn't exist

    @return The setting's value.
    """

    return dotted_get(get_settings_object(), dotted, default)


def get_timestamp() -> float:
    """
    @brief Get the current timestamp (in second).

    @return The timestamp.
    """

    return time.time()


def get_setting_renderer_interval() -> int:
    """
    @brief Get the renderer interval.

    @return The renderer interval.
    """

    interval = get_setting("renderer_interval", 250)

    if interval < 0:
        interval = sys.maxsize

    # a minimum for not crashing the system accidentally
    return int(max(30, interval))


def get_setting_show_open_button(view: sublime.View) -> str:
    from .functions import is_view_too_large

    return get_setting(
        "show_open_button_fallback"
        if not view.is_loading() and is_view_too_large(view)
        else "show_open_button"
    )
