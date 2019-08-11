import base64
import mimetypes
import os
import sublime
import time
from .log import msg


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

    img_path = get_image_path(img_name)
    img_ext = os.path.splitext(img_path)[1]

    try:
        img_base64 = base64.b64encode(sublime.load_binary_resource(img_path)).decode()
    except IOError:
        img_base64 = ""
        print(msg("Resource not found: " + img_path))

    img_mime = mimetypes.types_map.get(img_ext, "")

    if not img_mime:
        print(msg("Cannot determine MIME type: " + img_path))

    img_data_uri = "data:{mime};base64,{base64}".format(mime=img_mime, base64=img_base64)

    # fmt: off
    return {
        "base64": img_base64,
        "data_uri": img_data_uri,
        "ext": img_ext,
        "mime": img_mime,
        "path": img_path,
    }
    # fmt: on


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
