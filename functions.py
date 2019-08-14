import io
import re
import sublime
import webbrowser
from collections.abc import Iterable
from .libs import png, triegex
from .log import msg
from .settings import get_setting


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
    view: sublime.View, regions: Iterable, search_radius: int = 200
) -> list:
    """
    @brief Found intersected URI regions from view by regions

    @param view    The view
    @param regions The regions

    @return list[sublime.Region] Found URI regions
    """

    regions = sorted(map(region_into_st_region_form, regions))
    search_regions = simplify_intersected_regions(
        (region_expand(region, search_radius) for region in regions), True
    )

    uri_regex_obj = get_uri_regex_object()
    uri_regions = []

    for region in search_regions:
        coordinate_bias = max(0, region.begin())

        uri_regions.extend(
            # convert "finditer()" coordinate into ST's coordinate
            sublime.Region(*region_shift(m.span(), coordinate_bias))
            for m in uri_regex_obj.finditer(view.substr(region))
        )

    # only pick up "uri_region"s that are intersected with "regions"
    # note that both "regions" and "uri_regions" are guaranteed sorted here
    regions_idx = 0
    uri_regions_intersected = []

    for uri_region in uri_regions:
        for idx in range(regions_idx, len(regions)):
            region = regions[idx]

            # later "uri_region" is always even larger so this "idx" is useless since now
            if uri_region.begin() > region.end():
                regions_idx = idx + 1

            if is_regions_intersected(uri_region, region, True):
                uri_regions_intersected.append(uri_region)

                break

    return uri_regions_intersected


def view_find_all_fast(view: sublime.View, regex_obj, return_st_region: bool = True) -> list:
    """
    @brief A faster/simpler implementation of View.find_all().

    @param view             the View object
    @param regex_obj        the compiled regex object
    @param return_st_region return region in sublime.Region type

    @return list[Union[sublime.Region, list[int]]]
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

    @return list[list[int]] the new "uri_regions" in the view
    """

    uri_regions = view_find_all_fast(view, uri_regex_obj, False)

    view_uri_regions_val(view, uri_regions)

    return uri_regions


def view_uri_regions_val(view: sublime.View, uri_regions=...):
    """
    @brief Set/Get the URI regions (in list of lists) of the current view

    @param view        The view
    @param uri_regions The URI regions (... = get mode, otherwise = set mode)

    @return Optional[list[list[int]]] None if the set mode, otherwise the URI regions
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

    @return Optional[float] None if the set mode, otherwise the value
    """

    if timestamp_s is ...:
        return view.settings().get("OUIB_last_update_timestamp", False)

    view.settings().set("OUIB_last_update_timestamp", timestamp_s)


def region_shift(region, shift: int):
    """
    @brief Shift the region by given amount.

    @param region The region
    @param shift  The shift

    @return the shifted region
    """

    if isinstance(region, int) or isinstance(region, float):
        return region + shift

    if isinstance(region, sublime.Region):
        return sublime.Region(region.a + shift, region.b + shift)

    return [region[0] + shift, region[-1] + shift]


def region_expand(region, expansion):
    """
    @brief Expand the region by given amount.

    @param region    The region
    @param expansion Union[int, list[int]] The amount of left/right expansion

    @return the expanded region
    """

    if isinstance(expansion, int) or isinstance(expansion, float):
        expansion = [int(expansion)] * 2

    if len(expansion) == 0:
        expansion = [0, 0]

    if len(expansion) == 1:
        # do not modify the input variable by "expansion *= 2"
        expansion = [expansion[0]] * 2

    if isinstance(region, int) or isinstance(region, float):
        return [region - expansion[0], region + expansion[1]]

    if isinstance(region, sublime.Region):
        return sublime.Region(region.begin() - expansion[0], region.end() + expansion[1])

    # fmt: off
    return [
        min(region[0], region[-1]) - expansion[0],
        max(region[0], region[-1]) + expansion[1],
    ]
    # fmt: on


def region_into_list_form(region, sort_result: bool = False) -> list:
    """
    @brief Convert the "region" into list form

    @param region      The region
    @param sort_result Sort the region

    @return list[int] the "region" in list form
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

    @return list[sublime.Region] the "region" in ST's region form
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


def simplify_intersected_regions(regions: Iterable, allow_boundary: bool = False) -> list:
    """
    @brief Simplify intersected regions by merging them into one region.

    @param regions        Iterable[sublime.Region] The regions
    @param allow_boundary Treat boundary contact as intersected

    @return list[sublime.Region] Simplified regions
    """

    merged_regions = []
    for region in sorted(regions):
        if not merged_regions:
            merged_regions.append(region)

            continue

        region_prev = merged_regions[-1]

        if is_regions_intersected(region_prev, region, allow_boundary):
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

    # treat boundary contact as intersected
    if allow_boundary:
        # left/right begin/end = l/r b/e
        lb_, le_ = region_1.begin(), region_1.end()
        rb_, re_ = region_2.begin(), region_2.end()

        if lb_ == rb_ or lb_ == re_ or le_ == rb_ or le_ == re_:
            return True

    return region_1.intersects(region_2)


def change_png_bytes_color(img_bytes: bytes, color_code: str) -> bytes:
    """
    @brief Change all colors in the PNG bytes to the new color.

    @param img_bytes  The PNG image bytes
    @param color_code The color code

    @return Color-changed PNG image bytes.
    """

    IMG_RGBA_CHANNELS = 4

    if not color_code:
        return img_bytes

    if not re.match(r"#(?:[0-9a-f]{6}|[0-9a-f]{8})$", color_code, re.IGNORECASE):
        raise ValueError("Invalid color code: " + color_code)

    color_code = color_code.lstrip("#")

    if len(color_code) == 6:
        color_code += "ff"  # default opaque

    r, g, b, a = [int(color_code[i : i + 2], 16) for i in range(0, 8, 2)]
    w, h, rows_src, img_info = png.Reader(bytes=img_bytes).asRGBA()

    rows_dst = []
    for row_src in rows_src:
        row_dst = []
        for i in range(0, len(row_src), IMG_RGBA_CHANNELS):
            row_dst.extend([r, g, b, int(row_src[i + 3] * a / 0xFF)])
        rows_dst.append(row_dst)

    buf = io.BytesIO()
    png.from_array(rows_dst, "RGBA").write(buf)

    return buf.getvalue()
