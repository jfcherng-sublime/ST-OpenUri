import re
import sublime
import webbrowser
from .libs import triegex
from .log import msg
from .settings import get_setting
from collections.abc import Iterable


def open_uri_from_browser(uri: str, browser=...) -> None:
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
    except Exception as e:
        sublime.error_message(
            'Failed to open browser "{browser}" to "{uri}" because {reason}'.format(
                browser=browser, uri=uri, reason=e
            )
        )


def get_uri_regex_object():
    """
    @brief Get the compiled regex object for matching URIs.

    @return The compiled regex object
    """

    # fmt: off
    schemes = {
        scheme
        for scheme, enabled in get_setting("detect_schemes").items()
        if enabled
    }
    # fmt: on

    scheme_matcher = (
        triegex.Triegex(*map(re.escape, schemes))
        .to_regex()
        .replace(r"\b", "")
        .replace(r"|~^(?#match nothing)", "")
    )

    path_matcher = get_setting("uri_path_regex").lstrip("^").rstrip("$")

    # our goal is to find URIs ASAP rather than validate them
    regex = r"\b{scheme}\b{path}".format(scheme=scheme_matcher, path=path_matcher)

    try:
        return re.compile(regex, re.IGNORECASE)
    except Exception as e:
        sublime.error_message(
            msg(
                "Cannot compile regex `{regex}` because `{reason}`. "
                'Please check "uri_path_regex" in plugin settings.'.format(regex=regex, reason=e)
            )
        )


def find_uri_regions_by_region(view: sublime.View, region, search_radius: int = 200) -> list:
    """
    @brief Found intersected URI regions from view by the region

    @param view   The view
    @param region The region

    @return list[sublime.Region] Found URI regions
    """

    return find_uri_regions_by_regions(view, [region], search_radius)


def find_uri_regions_by_regions(
    view: sublime.View, regions: list, search_radius: int = 200
) -> list:
    """
    @brief Found intersected URI regions from view by regions

    @param view    The view
    @param regions The regions

    @return list[sublime.Region] Found URI regions
    """

    regions = list(map(region_into_st_region_form, regions))
    search_regions = simplify_intersected_regions(
        [
            sublime.Region(region.begin() - search_radius, region.end() + search_radius)
            for region in regions
        ]
    )

    uri_regex_obj = get_uri_regex_object()
    uri_regions = []

    for region in search_regions:
        coordinate_bias = max(0, region.begin())
        content = view.substr(region)

        for m in uri_regex_obj.finditer(content):
            uri_regions.append(
                # convert "finditer()" coordinate into ST's coordinate
                region_shift(sublime.Region(*m.span()), coordinate_bias)
            )

    # remove "uri_region"s that are not intersected with "regions"
    # todo: we can sort "regions" and use binary searching for "any(is_regions_intersected())"
    return [
        uri_region
        for uri_region in uri_regions
        if any(is_regions_intersected(uri_region, region, True) for region in regions)
    ]


def view_find_all_fast(view: sublime.View, regex_obj, return_st_region: bool = True) -> list:
    """
    @brief A faster/simpler implementation of View.find_all().

    @param view             the View object
    @param regex_obj        the compiled regex object
    @param return_st_region return region in sublime.Region type

    @return sublime.Region[]|list[]
    """

    regions = [m.span() for m in regex_obj.finditer(view.substr(sublime.Region(0, view.size())))]

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


def view_uri_regions_val(view: sublime.View, uri_regions=...):
    """
    @brief Set/Get the URI regions (in list of lists) of the current view

    @param view        The view
    @param uri_regions The URI regions (... = get mode, otherwise = set mode)

    @return None|list[] None if the set mode, otherwise the URI regions
    """

    if uri_regions is ...:
        return view.settings().get("OUIB_uri_regions", [])

    uri_regions = [region_into_list_form(r, True) for r in uri_regions]

    view.settings().set("OUIB_uri_regions", uri_regions)


def view_last_update_timestamp_val(view: sublime.View, timestamp_s=...):
    """
    @brief Set/Get the last timestamp (in sec) when "OUIB_uri_regions" is updated

    @param view        The view
    @param timestamp_s The last timestamp (in sec)

    @return None|float None if the set mode, otherwise the value
    """

    if timestamp_s is ...:
        return view.settings().get("OUIB_last_update_timestamp", False)

    view.settings().set("OUIB_last_update_timestamp", timestamp_s)


def region_shift(region, shift: int):
    if isinstance(region, int) or isinstance(region, float):
        return region + shift

    if isinstance(region, sublime.Region):
        return sublime.Region(region.a + shift, region.b + shift)

    return [region[0] + shift, region[-1] + shift]


def region_into_list_form(region, sort_result: bool = False) -> list:
    """
    @brief Convert the "region" into list form

    @param region      The region
    @param sort_result Sort the region

    @return list the "region" in list form
    """

    if isinstance(region, sublime.Region):
        region = [region.a, region.b]
    elif isinstance(region, int) or isinstance(region, float):
        region = [int(region)] * 2
    elif isinstance(region, Iterable) and not isinstance(region, list):
        region = list(region)

    assert isinstance(region, list)

    if not region:
        raise ValueError("region must not be empty.")

    if len(region) > 0:
        region = [region[0], region[-1]]

    return sorted(region) if sort_result else region


def region_into_st_region_form(region, sort_result: bool = False) -> list:
    """
    @brief Convert the "region" into ST's region form

    @param region      The region
    @param sort_result Sort the region

    @return list the "region" in ST's region form
    """

    if isinstance(region, int) or isinstance(region, float):
        region = [int(region)] * 2
    elif isinstance(region, Iterable) and not isinstance(region, list):
        region = list(region)

    if isinstance(region, list) and not region:
        raise ValueError("region must not be empty.")

    if not isinstance(region, sublime.Region):
        region = sublime.Region(region[0], region[-1])

    return sublime.Region(region.begin(), region.end()) if sort_result else region


def simplify_intersected_regions(regions: list) -> list:
    """
    @brief Simplify intersected regions by merging them into one region.

    @param regions list[sublime.Region] The regions

    @return list[sublime.Region] Simplified regions
    """

    merged_regions = []
    for region in sorted(regions):
        if not merged_regions:
            merged_regions.append(region)

            continue

        region_prev = merged_regions[-1]

        if is_regions_intersected(region_prev, region, True):
            merged_regions[-1] = sublime.Region(region_prev.begin(), region.end())
        else:
            merged_regions.append(region)

    return merged_regions


def is_regions_intersected(
    region_1: sublime.Region, region_2: sublime.Region, allow_boundary: bool = False
) -> bool:
    """
    @brief Check whether two regions are intersected.

    @param region_1       The 1st region
    @param region_2       The 2nd region
    @param allow_boundary Treat boundary contact as intersected

    @return True if intersected, False otherwise.
    """

    # left/right begin/end = l/r b/e
    lb_, le_ = region_1.begin(), region_1.end()
    rb_, re_ = region_2.begin(), region_2.end()

    # treat boundary contact as intersected
    if allow_boundary and (lb_ == rb_ or lb_ == re_ or le_ == rb_ or le_ == re_):
        return True

    return region_1.intersects(region_2)
