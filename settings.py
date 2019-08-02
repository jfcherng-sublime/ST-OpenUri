import mimetypes
import os
import sublime
import time
from .functions import bytes_to_base64_str, msg


def get_package_name() -> str:
    return __package__


def get_package_path() -> str:
    return "Packages/" + get_package_name()


def get_image_path(img_name: str) -> str:
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
    img_path = get_image_path(img_name)
    img_ext = os.path.splitext(img_path)[1]

    try:
        img_base64 = bytes_to_base64_str(sublime.load_binary_resource(img_path))
    except IOError:
        img_base64 = ""
        print(msg("Resource not found: " + img_path))

    img_mime = mimetypes.types_map.get(img_ext, "")

    if not img_mime:
        print(msg("Cannot determine MIME type: " + img_path))

    return {"base64": img_base64, "mime": img_mime, "path": img_path}


def get_settings_file() -> str:
    """
    hard-coded workaround for different package name
    due to installation via Package Control: Add Repository
    """

    return "OpenUriInBrowser.sublime-settings"


def get_settings_object() -> sublime.Settings:
    return sublime.load_settings(get_settings_file())


def get_setting(key: str, default=None):
    return get_settings_object().get(key, default)


def get_timestamp() -> float:
    return time.time()


def get_uri_regex_by_schemes(schemes=None) -> str:
    if schemes is None:
        schemes = get_setting("detect_schemes")

    scheme_regexes = [
        "(?:{protocols}){delimiter}".format(protocols="|".join(set(protocols)), delimiter=delimiter)
        for delimiter, protocols in schemes.items()
    ]

    scheme_regex = "(?:{regex})".format(regex="|".join(scheme_regexes))

    # our goal is to find URIs ASAP rather than validate them
    return r"\b" + scheme_regex + r"[A-Za-z0-9@~_+\-*/&=#%|:.,?]+(?<=[A-Za-z0-9@~_+\-*/&=#%|])"
