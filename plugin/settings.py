from .constant import PLUGIN_NAME
from .constant import SETTINGS_FILE_NAME
from .libs import imagesize
from .logger import log
from .types import ImageDict
from typing import Any, Dict, Optional
import base64
import os
import sublime
import tempfile
import time


def get_expanding_variables(window: Optional[sublime.Window]) -> Dict[str, str]:
    variables: Dict[str, Any] = {
        "home": os.path.expanduser("~"),
        "package_name": PLUGIN_NAME,
        "package_path": f"Packages/{PLUGIN_NAME}",
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

    return sublime.expand_variables(
        get_setting("image_files")[img_name],
        get_expanding_variables(sublime.active_window()),
    )


def get_image_info(img_name: str) -> ImageDict:
    """
    @brief Get image informations of an image from plugin settings.

    @param img_name The image name

    @return The image information.
    """
    img_path = get_image_path(img_name)
    img_ext = os.path.splitext(img_path)[1]
    img_mime = "image/png"

    assert img_ext.lower() == ".png"

    try:
        img_bytes = sublime.load_binary_resource(img_path)
    except IOError:
        img_bytes = b""
        log("error", f"Resource not found: {img_path}")

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

    return color_code_to_rgba(get_setting("image_colors")[img_name], region)


def get_settings_object() -> sublime.Settings:
    """
    @brief Get the plugin settings object. This function will call `sublime.load_settings()`.

    @return The settings object.
    """

    return sublime.load_settings(SETTINGS_FILE_NAME)


def get_setting(dotted: str, default: Optional[Any] = None) -> Any:
    """
    @brief Get the plugin setting with the dotted key.

    @param dotted  The dotted key
    @param default The default value if the key doesn't exist

    @return The setting's value.
    """

    from .shared import global_get

    return global_get(f"settings.{dotted}", default)


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

    if (interval := get_setting("renderer_interval", 250)) < 0:
        interval = float("inf")

    # a minimum for not crashing the system accidentally
    return int(max(30, interval))


def get_setting_show_open_button(view: sublime.View) -> str:
    from .functions import is_view_too_large

    return get_setting(
        # ...
        "show_open_button_fallback"
        if not view.is_loading() and is_view_too_large(view)
        else "show_open_button"
    )
