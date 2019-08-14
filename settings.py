import base64
import os
import sublime
import time
from .log import msg

HAS_API_VIEW_STYLE_FOR_SCOPE = int(sublime.version()) >= 3170


def get_package_name() -> str:
    """
    @brief Getsthe package name.

    @return The package name.
    """

    return __package__


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

    img_path = get_setting("image_" + img_name)

    assert isinstance(img_path, str)

    return sublime.expand_variables(
        img_path,
        {
            # fmt: off
            "package": get_package_name(),
            "package_path": get_package_path(),
            # fmt: on
        },
    )


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
        print(msg("Resource not found: " + img_path))

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


def get_colored_image_base64(img_name: str, rgba_code: str) -> str:
    """
    @brief Get the colored image in base64 string.

    @param img_name  The image name
    @param rgba_code The color code in #RRGGBBAA

    @return The image base64 string
    """

    from .functions import change_png_bytes_color
    from .Globals import Globals

    if not rgba_code:
        return getattr(Globals, "image_" + img_name)["base64"]

    cache_key = "{name}@{color}".format(name=img_name, color=rgba_code)

    if cache_key not in Globals.colored_image_base64:
        img_bytes = getattr(Globals, "image_" + img_name)["bytes"]
        img_bytes = change_png_bytes_color(img_bytes, rgba_code)
        img_base64 = base64.b64encode(img_bytes).decode()

        Globals.colored_image_base64[cache_key] = img_base64

    return Globals.colored_image_base64[cache_key]


def get_settings_file() -> str:
    """
    @brief Get the settings file name.

    @return The settings file name.
    """

    return "OpenUriInBrowser.sublime-settings"


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
