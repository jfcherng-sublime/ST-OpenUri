import bisect
import re
import sublime
import webbrowser
from .libs import triegex
from .settings import get_setting


def open_uri_from_browser(uri: str, browser=None) -> None:
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


def generate_uri_regex_by_schemes(schemes: list) -> str:
    """
    @brief Generate a regex for matching URIs by given schemes.

    @param schemes The schemes

    @return The generated regex string
    """

    scheme_matcher = (
        triegex.Triegex(*map(re.escape, set(schemes)))
        .to_regex()
        .replace(r"\b", "")
        .replace(r"|~^(?#match nothing)", "")
    )

    # our goal is to find URIs ASAP rather than validate them
    return r"\b" + scheme_matcher + r"\b[a-z0-9@~_+\-*/&=#%|:.,!?]+(?<=[a-z0-9@~_+\-*/&=#%|])"


def find_uri_regions_by_region(view: sublime.View, region) -> list:
    """
    @brief Found intersected URI regions from view by region

    @param view   The view
    @param region The region

    @return list[] Found URI regions
    """

    view_uri_regions = view_uri_regions_val(view)

    if not view_uri_regions:
        return []

    region = region_into_list_form(region, True)

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


def find_uri_regions_by_regions(view: sublime.View, regions: list) -> list:
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


def view_find_all_fast(view: sublime.View, regex_obj, return_st_region: bool = True) -> list:
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


def view_update_uri_regions(view: sublime.View, uri_regex_obj) -> list:
    """
    @brief Update view's "uri_regions" variable

    @param view          The view
    @param uri_regex_obj The URI regex obj

    @return the new "uri_regions" in the view
    """

    uri_regions = view_find_all_fast(view, uri_regex_obj, False)

    view_uri_regions_val(view, uri_regions)

    return uri_regions


def view_uri_regions_val(view: sublime.View, uri_regions=None):
    """
    @brief Set/Get the URI regions (in list of lists) of the current view

    @param view        The view
    @param uri_regions The URI regions (None = get mode, otherwise = set mode)

    @return None|list[] None if the set mode, otherwise the URI regions
    """

    if uri_regions is None:
        return view.settings().get("OUIB_uri_regions", [])

    uri_regions = [region_into_list_form(r, True) for r in uri_regions]

    view.settings().set("OUIB_uri_regions", uri_regions)


def view_typing_timestamp_val(view: sublime.View, timestamp_s=None):
    """
    @brief Set/Get the URI regions (in list of lists) of the current view

    @param view        The view
    @param timestamp_s The last timestamp (in sec) when the user is typing

    @return None|float None if the set mode, otherwise the value
    """

    if timestamp_s is None:
        return view.settings().get("OUIB_typing_timestamp", False)

    view.settings().set("OUIB_typing_timestamp", timestamp_s)


def region_into_list_form(region, sort_result: bool = False) -> list:
    """
    @brief Convert the "region" into list form

    @param region      The region
    @param sort_result Sort the region

    @return list the "region" into list form
    """

    if isinstance(region, sublime.Region):
        region = [region.a, region.b]
    elif isinstance(region, int) or isinstance(region, float):
        region = [int(region)] * 2
    elif hasattr(region, "__iter__") and not isinstance(region, list):
        region = list(region)

    assert isinstance(region, list)

    if not region:
        raise ValueError("region must not be empty.")

    if len(region) == 1:
        region *= 2
    elif len(region) > 2:
        region = region[0:2]

    return sorted(region) if sort_result else region


def is_intersected(region_1, region_2, allow_pointy_boundary: bool = False) -> bool:
    """
    @brief Check whether two regions are intersected.

    @param region_1              The 1st region
    @param region_2              The 2nd region
    @param allow_pointy_boundary Treat pointy boundary as intersected

    @return True if intersected, False otherwise.
    """

    # left/right begin/end = l/r b/e
    lb_, le_ = region_into_list_form(region_1, True)
    rb_, re_ = region_into_list_form(region_2, True)

    # one of the region is actually a point and it's on the other region's boundary
    if allow_pointy_boundary and (
        lb_ == rb_ == re_ or le_ == rb_ == re_ or rb_ == lb_ == le_ or re_ == lb_ == le_
    ):
        return True

    return (
        (lb_ == rb_ and le_ == re_)
        or (rb_ > lb_ and rb_ < le_)
        or (re_ > lb_ and re_ < le_)
        or (lb_ > rb_ and lb_ < re_)
        or (le_ > rb_ and le_ < re_)
    )
