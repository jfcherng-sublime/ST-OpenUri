from __future__ import annotations

import base64
import tempfile
from pathlib import Path
from typing import Any

import sublime

from .constants import PLUGIN_NAME, SETTINGS_FILE_NAME
from .libs import imagesize
from .logger import log
from .shared import global_get
from .types import ImageDict
from .utils import get_timestamp, view_last_typing_timestamp_val


def get_expanding_variables(window: sublime.Window | None) -> dict[str, str]:
    variables: dict[str, Any] = {
        "home": str(Path.home()),
        "package_name": PLUGIN_NAME,
        "package_path": f"Packages/{PLUGIN_NAME}",
        "temp_dir": tempfile.gettempdir(),
    }

    if window:
        variables.update(window.extract_variables())

    return variables


def get_settings_object() -> sublime.Settings:
    """
    @brief Get the plugin settings object. This function will call `sublime.load_settings()`.

    @return The settings object.
    """
    return sublime.load_settings(SETTINGS_FILE_NAME)


def get_setting(dotted: str, default: Any | None = None) -> Any:
    """
    @brief Get the plugin setting with the dotted key.

    @param dotted  The dotted key
    @param default The default value if the key doesn't exist

    @return The setting's value.
    """
    return global_get(f"settings.{dotted}", default)


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
    img_ext = Path(img_path).suffix
    img_mime = "image/png"

    assert img_ext.lower() == ".png"

    try:
        img_bytes = sublime.load_binary_resource(img_path)
    except OSError:
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
    return get_setting(
        "show_open_button_fallback" if not view.is_loading() and is_view_too_large(view) else "show_open_button"
    )


def is_view_too_large(view: sublime.View) -> bool:
    """
    @brief Determine if the view is too large. Note that size will be `0` if the view is loading.

    @param view The view

    @return `True` if the view is too large, `False` otherwise.
    """
    return view.size() > get_setting("large_file_threshold")


def is_view_typing(view: sublime.View) -> bool:
    """
    @brief Determine if the view typing.

    @param view The view

    @return `True` if the view is typing, `False` otherwise.
    """
    now_s = get_timestamp()
    last_typing_s = view_last_typing_timestamp_val(view) or 0

    return (now_s - last_typing_s) * 1000 < get_setting("typing_period")
