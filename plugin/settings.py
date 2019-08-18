import base64
import os
import sublime
import time
from .Globals import global_get, global_set


def get_package_name() -> str:
    """
    @brief Getsthe package name.

    @return The package name.
    """

    # __package__ will be "XXX.plugin" under this folder structure
    # so I just have it hard-coded, sadly :/
    return "OpenUriInBrowser"


def get_package_path() -> str:
    """
    @brief Gets the package path.

    @return The package path.
    """

    return "Packages/" + get_package_name()


def get_image_path(img_name: str) -> str:
    """
    @brief Get the image resource path from plugin settings.

    @param img_name The image name

    @return The image resource path.
    """

    img_path = get_setting("image_files")[img_name]

    # assert for potential dev code typos
    assert isinstance(img_path, str)

    return sublime.expand_variables(
        img_path,
        {
            # fmt: off
            "package_name": get_package_name(),
            "package_path": get_package_path(),
            # fmt: on
        },
    )


def get_image_color(img_name: str, region: sublime.Region) -> str:
    """
    @brief Get the image color from plugin settings in the form of #RRGGBBAA.

    @param img_name The image name
    @param region   The region

    @return The color code in the form of #RRGGBBAA
    """

    from .functions import color_code_to_rgba

    img_color = get_setting("image_colors")[img_name]

    # assert for potential dev code typos
    assert isinstance(img_color, str)

    return color_code_to_rgba(img_color, region)


def get_image_info(img_name: str) -> dict:
    """
    @brief Get image informations of an image from plugin settings.

    @param img_name The image name

    @return Dict[str, Any] The image information.
    """

    from .libs import imagesize

    img_path = get_image_path(img_name)
    img_ext = os.path.splitext(img_path)[1]
    img_mime = "image/png"

    assert img_ext.lower() == ".png"

    try:
        img_bytes = sublime.load_binary_resource(img_path)
    except IOError:
        global_get("logger").error("Resource not found: " + img_path)

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


def get_colored_image_base64_by_color(img_name: str, rgba_code: str) -> str:
    """
    @brief Get the colored image in base64 string by RGBA color code.

    @param img_name  The image name
    @param rgba_code The color code in #RRGGBBAA

    @return The image base64 string
    """

    from .functions import change_png_bytes_color

    cache_key = "{name};{color}".format(name=img_name, color=rgba_code)

    if not rgba_code:
        return global_get("images.%s.base64" % img_name)

    cached = "images.@cache.%s" % cache_key

    if global_get(cached, None) is None:
        img_bytes = global_get("images.%s.bytes" % img_name)
        img_bytes = change_png_bytes_color(img_bytes, rgba_code)
        img_base64 = base64.b64encode(img_bytes).decode()

        global_set(cached, img_base64)

    return global_get(cached)


def get_colored_image_base64_by_region(img_name: str, region: sublime.Region) -> str:
    """
    @brief Get the colored image in base64 string by region.

    @param img_name The image name
    @param region   The region

    @return The image base64 string
    """

    return get_colored_image_base64_by_color(img_name, get_image_color(img_name, region))


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


def get_setting(key: str, default=None):
    """
    @brief Get the plugin setting with the key.

    @param key     The key
    @param default The default value if the key doesn't exist

    @return Optional[Any] The setting's value.
    """

    return get_settings_object().get(key, default)


def get_timestamp() -> float:
    """
    @brief Get the current timestamp (in second).

    @return The timestamp.
    """

    return time.time()
