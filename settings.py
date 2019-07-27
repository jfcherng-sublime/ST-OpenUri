import sublime


def get_package_name():
    return __package__


def get_package_path():
    return "Packages/" + get_package_name()


def get_image_path():
    return sublime.expand_variables(
        get_setting("image_new_window"),
        {
            # fmt: off
            "package": get_package_name(),
            "package_path": get_package_path(),
            # fmt: on
        },
    )


def get_settings_file():
    """
    hard-coded workaround for different package name
    due to installation via Package Control: Add Repository
    """

    return "OpenUrlInBrowser.sublime-settings"


def get_settings_object():
    return sublime.load_settings(get_settings_file())


def get_setting(key, default=None):
    return get_settings_object().get(key, default)


def get_url_regex_by_schemes(schemes=None):
    if schemes is None:
        schemes = get_setting("detect_schemes")

    scheme_regexes = [
        "(?:{protocols}){delimiter}".format(protocols="|".join(set(protocols)), delimiter=delimiter)
        for delimiter, protocols in schemes.items()
    ]

    scheme_regex = "(?:{regex})".format(regex="|".join(scheme_regexes))

    # our goal is to find URLs ASAP rather than validate them
    return r"\b" + scheme_regex + r"[A-Za-z0-9@~_+\-*/&=#%|:.,?]+(?<=[A-Za-z0-9@~_+\-*/&=#%|])"
