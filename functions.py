import bisect
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


def open_browser(url, browser=None):
    if browser is None:
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


def find_url_region_by_point(url_regions, point):
    if not url_regions:
        return None

    # since "url_regions" is auto sorted, we could perform a binary searching
    insert_idx = bisect.bisect_right(
        url_regions,
        [
            point,
            # this ending point is a trick for binary searching
            # extends the ending point to make it larger than any regions
            url_regions[-1][1] + 1,
        ],
    )

    # this is the only region which can possibly contain the hovered point
    region_check = url_regions[insert_idx - 1]

    return region_check if region_check[0] <= point <= region_check[1] else None


def view_find_all_fast(view, regex_obj):
    """
    @brief A faster/simpler implementation of View.find_all().

    @param view      the View object
    @param regex_obj the compiled regex object

    @return sublime.Region[]
    """

    iterator = regex_obj.finditer(view.substr(sublime.Region(0, view.size())))

    return [sublime.Region(*(m.span())) for m in iterator] if iterator else []


def view_url_regions_val(view, url_regions=None):
    """
    @brief Set/Get the URL regions (in list of lists) of the current view

    @param view        The view
    @param url_regions The url regions (None = get mode, otherwise = set mode)

    @return None|list[] None if the set mode, otherwise the URL regions
    """

    if url_regions is None:
        return view.settings().get("OIB_url_regions", [])

    # always convert sublime.Region into a list
    for idx, region in enumerate(url_regions):
        if isinstance(region, sublime.Region):
            url_regions[idx] = [region.begin(), region.end()]

    view.settings().set("OIB_url_regions", url_regions)
