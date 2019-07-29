import sublime
import time


def get_package_name() -> str:
    return __package__


def get_package_path() -> str:
    return "Packages/" + get_package_name()


def get_image_path() -> str:
    return sublime.expand_variables(
        get_setting("image_new_window"),
        {
            # fmt: off
            "package": get_package_name(),
            "package_path": get_package_path(),
            # fmt: on
        },
    )


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
