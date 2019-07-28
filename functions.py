import bisect
import sublime
import webbrowser
from .settings import get_setting


def open_uri_from_browser(uri, browser=None):
    """
    @brief Open the URI with the browser.

    @param uri     The uri
    @param browser The browser (None = default settings = system's default)
    """

    if not isinstance(browser, str):
        browser = get_setting("browser")

    if browser == "":
        browser = None

    try:
        # https://docs.python.org/3.3/library/webbrowser.html#webbrowser.get
        webbrowser.get(browser).open(uri, autoraise=True)
    except (webbrowser.Error):
        sublime.error_message(
            'Failed to open browser "{browser}" for "{uri}".'.format(browser=browser, uri=uri)
        )


def find_uri_regions_by_region(view, region):
    """
    @brief Found intersected URI regions from view by region

    @param view   The view
    @param region The region

    @return list[] Found URI regions
    """

    view_uri_regions = view_uri_regions_val(view)

    if not view_uri_regions:
        return []

    if isinstance(region, sublime.Region):
        region = [region.begin(), region.end()]
    elif isinstance(region, int):
        region = [region, region]
    elif isinstance(region, tuple):
        region = list(tuple)

    assert isinstance(region, list)

    # since "view_uri_regions" is auto sorted, we could perform a binary searching
    insert_idx = bisect.bisect_left(view_uri_regions, region)

    # at most, there are 3 URI regions that are possibly intersected with "region"
    possible_idxs = filter(
        # fmt: off
        lambda idx: 0 <= idx < len(view_uri_regions),
        [insert_idx - 1, insert_idx, insert_idx + 1]
        # fmt: on
    )

    return [
        view_uri_regions[idx]
        for idx in possible_idxs
        if is_intersected(view_uri_regions[idx], region, True)
    ]


def find_uri_regions_by_regions(view, regions):
    """
    @brief Found intersected URI regions from view by regions

    @param view    The view
    @param regions The regions

    @return list[] Found URI regions
    """

    uri_regions = []
    for region in regions:
        uri_regions.extend(find_uri_regions_by_region(view, region))
    uri_regions.sort()

    # remove duplicated regions
    return [
        uri_regions[idx]
        for idx in range(len(uri_regions))
        if idx == 0 or uri_regions[idx] != uri_regions[idx - 1]
    ]


def view_find_all_fast(view, regex_obj, return_st_region=True):
    """
    @brief A faster/simpler implementation of View.find_all().

    @param view             the View object
    @param regex_obj        the compiled regex object
    @param return_st_region return region in sublime.Region type

    @return sublime.Region[]|list[]
    """

    iterator = regex_obj.finditer(view.substr(sublime.Region(0, view.size())))
    regions = [m.span() for m in iterator] if iterator else []

    if return_st_region:
        regions = [sublime.Region(*r) for r in regions]

    return regions


def view_update_uri_regions(view, URI_REGEX_OBJ):
    uri_regions = view_find_all_fast(view, URI_REGEX_OBJ, False)

    # update found URI regions
    view_uri_regions_val(view, uri_regions)

    return uri_regions


def view_uri_regions_val(view, uri_regions=None):
    """
    @brief Set/Get the URI regions (in list of lists) of the current view

    @param view        The view
    @param uri_regions The URI regions (None = get mode, otherwise = set mode)

    @return None|list[] None if the set mode, otherwise the URI regions
    """

    if uri_regions is None:
        return view.settings().get("OUIB_uri_regions", [])

    # always convert sublime.Region into a list
    for idx, region in enumerate(uri_regions):
        if isinstance(region, sublime.Region):
            uri_regions[idx] = [region.begin(), region.end()]

    view.settings().set("OUIB_uri_regions", uri_regions)


def view_typing_timestamp_val(view, timestamp_s=None):
    """
    @brief Set/Get the URI regions (in list of lists) of the current view

    @param view        The view
    @param timestamp_s The last timestamp (in sec) when the user is typing

    @return None|float None if the set mode, otherwise the value
    """

    if timestamp_s is None:
        return view.settings().get("OUIB_typing_timestamp", False)

    view.settings().set("OUIB_typing_timestamp", timestamp_s)


def is_intersected(region_1, region_2, allow_pointy_boundary=False):
    """
    @brief Check whether two regions are intersected.

    @param region_1              The 1st region
    @param region_2              The 2nd region
    @param allow_pointy_boundary Treat pointy boundary as intersected

    @return True if intersected, False otherwise.
    """

    lb = region_1.begin() if isinstance(region_1, sublime.Region) else min(region_1)
    le = region_1.end() if isinstance(region_1, sublime.Region) else max(region_1)
    rb = region_2.begin() if isinstance(region_2, sublime.Region) else min(region_2)
    re = region_2.end() if isinstance(region_2, sublime.Region) else max(region_2)

    # one of the region is actually a point and it's on the other region's boundary
    if allow_pointy_boundary and (
        lb == rb == re or le == rb == re or rb == lb == le or re == lb == le
    ):
        return True

    return (
        (lb == rb and le == re)
        or (rb > lb and rb < le)
        or (re > lb and re < le)
        or (lb > rb and lb < re)
        or (le > rb and le < re)
    )
