import io
import re
import sublime
import webbrowser
from collections.abc import Iterable
from .Globals import global_get
from .libs import png, triegex
from .log import log
from .settings import get_setting
from .utils import (
    is_regions_intersected,
    region_expand,
    region_into_list_form,
    region_into_st_region_form,
    region_shift,
    simple_decorator,
    simplify_intersected_regions,
    view_find_all_fast,
)


def open_uri_with_browser(uri: str, browser=...) -> None:
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
        log(
            "critical",
            'Failed to open browser "{browser}" to "{uri}" '
            "because {reason}".format(browser=browser, uri=uri, reason=e),
        )


def compile_uri_regex() -> tuple:
    """
    @brief Get the compiled regex object for matching URIs.

    @return (activated schemes, compiled regex object)
    """

    detect_schemes = get_setting("detect_schemes")
    uri_path_regexes = get_setting("uri_path_regexes")

    activated_schemes = []
    uri_regexes = []
    for scheme, scheme_settings in detect_schemes.items():
        if not scheme_settings.get("enabled", False):
            continue

        path_regex_name = scheme_settings.get("path_regex", "@default")
        if path_regex_name not in uri_path_regexes:
            log(
                "warning",
                'Ignore scheme "{scheme}" due to invalid "path_regex": {path_regex}'.format(
                    scheme=scheme, path_regex=path_regex_name
                ),
            )
            continue

        activated_schemes.append(scheme)
        uri_regexes.append(re.escape(scheme) + r"(?:(?#{}))".format(path_regex_name))

    regex = r"\b" + (
        triegex.Triegex(*uri_regexes)
        .to_regex()
        .replace(r"\b", "")
        .replace(r"|~^(?#match nothing)", "")
    )

    log("debug", "Optimized URI matching regex (before expanding): {}".format(regex))

    # expand path regexes by their names
    for path_regex_name, path_regex in uri_path_regexes.items():
        regex = regex.replace(r"(?#{})".format(path_regex_name), path_regex)

    log("debug", "Optimized URI matching regex: {}".format(regex))

    try:
        regex_obj = re.compile(regex, re.IGNORECASE)
    except Exception as e:
        log(
            "critical",
            "Cannot compile regex `{regex}` because `{reason}`. "
            'Please check "uri_path_regex" in plugin settings.'.format(regex=regex, reason=e),
        )

    return regex_obj, sorted(activated_schemes)


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

    uri_regions = []
    for region in search_regions:
        coordinate_bias = max(0, region.begin())

        uri_regions.extend(
            # convert "finditer()" coordinate into ST's coordinate
            sublime.Region(*region_shift(m.span(), coordinate_bias))
            for m in global_get("uri_regex_obj").finditer(view.substr(region))
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


def view_update_uri_regions(view: sublime.View, uri_regex_obj) -> None:
    """
    @brief Update view's "uri_regions" variable

    @param view          The view
    @param uri_regex_obj The URI regex obj
    """

    view_uri_regions_val(view, view_find_all_fast(view, uri_regex_obj, False))


def view_uri_regions_val(view: sublime.View, uri_regions=...):
    """
    @brief Set/Get the URI regions (in list of lists) of the current view

    @param view        The view
    @param uri_regions The URI regions (... = get mode, otherwise = set mode)

    @return Optional[list[list[int]]] None if the set mode, otherwise the URI regions
    """

    if uri_regions is ...:
        return view.settings().get("OUIB_uri_regions", [])

    view.settings().set("OUIB_uri_regions", [region_into_list_form(r, True) for r in uri_regions])


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


def change_png_bytes_color(img_bytes: bytes, rgba_code: str) -> bytes:
    """
    @brief Change all colors in the PNG bytes to the new color.

    @param img_bytes The PNG image bytes
    @param rgba_code The color code in the form of #RRGGBBAA

    @return Color-changed PNG image bytes.
    """

    if not rgba_code:
        return img_bytes

    if not re.match(r"#[0-9a-fA-F]{8}$", rgba_code):
        raise ValueError("Invalid RGBA color code: " + rgba_code)

    def render_pixel(rgba_src: list, rgba_dst: list, invert_gray: bool = False) -> list:
        gray_ratio = calculate_gray(rgba_src) / 0xFF
        if invert_gray:
            gray_ratio = 1 - gray_ratio

        return [
            int(rgba_dst[0] * gray_ratio),
            int(rgba_dst[1] * gray_ratio),
            int(rgba_dst[2] * gray_ratio),
            int(rgba_dst[3] * rgba_src[3] / 0xFF),
        ]

    invert_gray = not is_img_light(img_bytes)  # invert for dark image to get a solid looking
    rgba_dst = [int(rgba_code[i : i + 2], 16) for i in range(1, 9, 2)]
    w, h, rows_src, img_info = png.Reader(bytes=img_bytes).asRGBA()

    rows_dst = []
    for row_src in rows_src:
        row_dst = []
        for i in range(0, len(row_src), 4):
            row_dst.extend(render_pixel(row_src[i : i + 4], rgba_dst, invert_gray))
        rows_dst.append(row_dst)

    buf = io.BytesIO()
    png.from_array(rows_dst, "RGBA").write(buf)

    return buf.getvalue()


def calculate_gray(rgb: list) -> list:
    """
    @brief Calculate the gray scale of a color.

    @param rgb The rgb color in list form

    @return The gray scale.
    """

    return (rgb[0] * 38 + rgb[1] * 75 + rgb[2] * 15) >> 7


def is_img_light(img_bytes: bytes) -> bool:
    """
    @brief Determine if image is light colored.

    @param img_bytes The image bytes

    @return True if image is light, False otherwise.
    """

    w, h, rows, img_info = png.Reader(bytes=img_bytes).asRGBA()

    gray_sum = 0
    for row in rows:
        for i in range(0, len(row), 4):
            gray_sum += calculate_gray(row[i : i + 4])

    return gray_sum * 2 > 0xFF * w * h


def add_alpha_to_rgb(color_code: str) -> str:
    """
    @brief Add the alpha part to a valid RGB color code (#RGB, #RRGGBB, #RRGGBBAA)

    @param color_code The color code

    @return The color code in the form of #RRGGBBAA
    """

    if not color_code:
        return ""

    rgb = color_code[1:9]  # strip "#" and possible extra chars

    # RGB to RRGGBB
    if len(rgb) == 3:
        rgb = rgb[0] * 2 + rgb[1] * 2 + rgb[2] * 2

    return "#" + (rgb + "ff")[:8].lower()


@simple_decorator(add_alpha_to_rgb)
def color_code_to_rgba(color_code: str, region: sublime.Region = sublime.Region(0, 0)) -> str:
    """
    @brief Convert user settings color code into #RRGGBBAA form

    @param color_code The color code string from user settings
    @param region     The scope-related region

    @return The color code in the form of #RRGGBBAA
    """

    if not color_code:
        return ""

    view = sublime.active_window().active_view()

    # "color_code" is a scope?
    if not color_code.startswith("#"):
        if global_get("HAS_API_VIEW_STYLE_FOR_SCOPE"):
            # "color" is guaranteed to be #RRGGBB or #RRGGBBAA
            color = view.style_for_scope(view.scope_name(region.end() - 1)).get("foreground", "")

            if color_code == "@scope":
                return color

            if color_code == "@scope_inverted":
                # strip "#" and make color into RRGGBBAA int
                rgba_int = int((color + "ff")[1:9], 16)
                # invert RRGGBB, remain AA, strip "0x" prefix from hex and prepend 0s until 8 chars
                return "#" + hex((~rgba_int & 0xFFFFFF00) | (rgba_int & 0xFF))[2:].zfill(8)

        return ""

    # now color code must starts with "#"
    rgb = color_code[1:9]  # strip "#" and possible extra chars

    # RGB, RRGGBB, RRGGBBAA are legal
    if len(rgb) in [3, 6, 8] and re.match(r"[0-9a-fA-F]+$", rgb):
        return "#" + rgb

    return ""
