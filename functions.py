import bisect
import sublime
import webbrowser
from .settings import get_setting


def open_url_from_browser(url, browser=None):
    """
    @brief Open the URL with the browser.

    @param url     The url
    @param browser The browser (None = default settings = system's default)
    """

    if not isinstance(browser, str):
        browser = get_setting("browser")

    if browser == "":
        browser = None

    try:
        # https://docs.python.org/3.3/library/webbrowser.html#webbrowser.get
        webbrowser.get(browser).open(url, autoraise=True)
    except (webbrowser.Error):
        sublime.error_message(
            'Failed to open browser "{browser}" for "{url}".'.format(browser=browser, url=url)
        )


def find_url_regions_by_region(view, region):
    """
    @brief Found intersected URL regions from view by region

    @param view   The view
    @param region The region

    @return list[] Found URL regions
    """

    view_url_regions = view_url_regions_val(view)

    if not view_url_regions:
        return []

    if isinstance(region, sublime.Region):
        region = [region.begin(), region.end()]
    elif isinstance(region, int):
        region = [region, region]
    elif isinstance(region, tuple):
        region = list(tuple)

    assert isinstance(region, list)

    # since "view_url_regions" is auto sorted, we could perform a binary searching
    insert_idx = bisect.bisect_left(view_url_regions, region)

    # at most, there are 3 URL regions that are possibly intersected with "region"
    possible_idxs = filter(
        # fmt: off
        lambda idx: 0 <= idx < len(view_url_regions),
        [insert_idx - 1, insert_idx, insert_idx + 1]
        # fmt: on
    )

    return [
        view_url_regions[idx]
        for idx in possible_idxs
        if is_intersected(view_url_regions[idx], region, True)
    ]


def find_url_regions_by_regions(view, regions):
    """
    @brief Found intersected URL regions from view by regions

    @param view    The view
    @param regions The regions

    @return list[] Found URL regions
    """

    url_regions = []
    for region in regions:
        url_regions.extend(find_url_regions_by_region(view, region))
    url_regions.sort()

    # remove duplicated regions
    return [
        url_regions[idx]
        for idx in range(len(url_regions))
        if idx == 0 or url_regions[idx] != url_regions[idx - 1]
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


def view_url_regions_val(view, url_regions=None):
    """
    @brief Set/Get the URL regions (in list of lists) of the current view

    @param view        The view
    @param url_regions The URL regions (None = get mode, otherwise = set mode)

    @return None|list[] None if the set mode, otherwise the URL regions
    """

    if url_regions is None:
        return view.settings().get("OUIB_url_regions", [])

    # always convert sublime.Region into a list
    for idx, region in enumerate(url_regions):
        if isinstance(region, sublime.Region):
            url_regions[idx] = [region.begin(), region.end()]

    view.settings().set("OUIB_url_regions", url_regions)


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
