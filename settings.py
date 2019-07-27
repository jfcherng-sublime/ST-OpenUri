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


def get_setting(key, default=None):
    return sublime.load_settings(get_settings_file()).get(key, default)
