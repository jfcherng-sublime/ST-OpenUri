import sublime
import webbrowser


def get_package_name():
    return __package__


def get_package_path():
    return "Packages/" + get_package_name()


def get_setting(key, default=None):
    settings = sublime.load_settings("OpenInBrowser.sublime-settings")
    return settings.get(key, default)


def get_image_path():
    return get_package_path() + "/" + get_setting("image_new_window")


def open_browser(url):
    browser = get_setting("custom_browser")

    if browser == "":
        browser = None

    try:
        # https://docs.python.org/3.3/library/webbrowser.html#webbrowser.get
        webbrowser.get(browser).open(url, autoraise=True)
    except (webbrowser.Error):
        sublime.error_message(
            'Failed to open browser "{browser}" for "{url}".'.format(browser=browser, url=url)
        )


def view_find_all_fast(view, regex_obj):
    """
    @brief A faster/simpler implementation of View.find_all().

    @param view      the View object
    @param regex_obj the compiled regex object

    @return sublime.Region[]
    """

    iterator = regex_obj.finditer(view.substr(sublime.Region(0, view.size())))

    return [sublime.Region(*(m.span())) for m in iterator] if iterator else []
