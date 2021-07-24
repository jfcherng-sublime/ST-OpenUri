from ..libs import triegex
from .log import log
from .settings import get_setting
from .settings import get_timestamp
from .shared import global_get
from .types import RegionLike
from .utils import is_regions_intersected
from .utils import region_expand
from .utils import region_into_st_region_form
from .utils import region_shift
from .utils import simplify_intersected_regions
from typing import Any, Dict, Iterable, List, Tuple, Optional, Pattern, cast
import re
import sublime
import urllib.parse as urllib_parse
import webbrowser


def open_uri_with_browser(uri: str, browser: Optional[str] = "") -> None:
    """
    @brief Open the URI with the browser.

    @param uri     The uri
    @param browser The browser
    """

    parsed_uri = urllib_parse.urlparse(uri)

    log("debug", f"Parsed URI: {parsed_uri}")

    # decode URL-encoded "file" scheme such as
    # "file:///D:/%E6%B8%AC%E8%A9%A6.html" -> "file:///D:/測試.html"
    if parsed_uri.scheme == "file":
        uri = urllib_parse.unquote(uri)

    if not browser:
        browser = get_setting("browser")

    # modify browser to None to use the system's default
    if browser == "":
        browser = None

    try:
        # https://docs.python.org/3.3/library/webbrowser.html#webbrowser.get
        webbrowser.get(browser).open(uri, autoraise=True)
    except Exception as e:
        log("critical", f'Failed to open browser "{browser}" to "{uri}" because {e}')


def compile_uri_regex() -> Tuple[Optional[Pattern[str]], Tuple[str, ...]]:
    """
    @brief Get the compiled regex object for matching URIs.

    @return (compiled regex object, activated schemes)
    """

    detect_schemes: Dict[str, Dict[str, Any]] = get_setting("detect_schemes")
    uri_path_regexes: Dict[str, str] = get_setting("uri_path_regexes")

    activated_schemes: List[str] = []
    uri_regexes: List[str] = []
    for scheme, scheme_settings in detect_schemes.items():
        if not scheme_settings.get("enabled", False):
            continue

        path_regex_name: str = scheme_settings.get("path_regex", "@default")
        if path_regex_name not in uri_path_regexes:
            log("warning", f'Ignore scheme "{scheme}" due to invalid "path_regex": {path_regex_name}')
            continue

        activated_schemes.append(scheme)
        uri_regexes.append(re.escape(scheme) + rf"(?:(?#{path_regex_name}))")

    # fmt: off
    regex: str = r"\b" + (
        triegex.Triegex(*uri_regexes)
        .to_regex()
        .replace(r"\b", "")  # type: ignore
        .replace(r"|~^(?#match nothing)", "")
    )
    # fmt: on

    log("debug", f"Optimized URI matching regex (before expanding): {regex}")

    # expand path regexes by their names
    for path_regex_name, path_regex in uri_path_regexes.items():
        regex = regex.replace(rf"(?#{path_regex_name})", path_regex)

    log("debug", f"Optimized URI matching regex: {regex}")

    regex_obj = None
    try:
        regex_obj = re.compile(regex, re.IGNORECASE)
    except Exception as e:
        log(
            "critical", f'Cannot compile regex `{regex}` because {e}. Please check "uri_path_regex" in plugin settings.'
        )

    return regex_obj, tuple(sorted(activated_schemes))


def find_uri_regions_by_region(
    view: sublime.View,
    region: RegionLike,
    search_radius: int = 200,
) -> List[sublime.Region]:
    """
    @brief Found intersected URI regions from view by the region

    @param view   The view
    @param region The region

    @return Found URI regions
    """

    return find_uri_regions_by_regions(view, (region,), search_radius)


def find_uri_regions_by_regions(
    view: sublime.View,
    regions: Iterable[RegionLike],
    search_radius: int = 200,
) -> List[sublime.Region]:
    """
    @brief Found intersected URI regions from view by regions

    @param view    The view
    @param regions The regions

    @return Found URI regions
    """

    st_regions = sorted(map(region_into_st_region_form, regions))

    search_regions = simplify_intersected_regions(
        (cast(sublime.Region, region_expand(region, search_radius)) for region in st_regions),
        True,
    )

    uri_regions: List[sublime.Region] = []
    for region in search_regions:
        coordinate_bias = max(0, region.begin())

        uri_regions.extend(
            # convert "finditer()" coordinate into ST's coordinate
            sublime.Region(*region_shift(m.span(), coordinate_bias))
            for m in global_get("uri_regex_obj").finditer(view.substr(region))
        )

    # only pick up "uri_region"s that are intersected with "st_regions"
    # note that both "st_regions" and "uri_regions" are guaranteed sorted here
    regions_idx = 0
    uri_regions_intersected: List[sublime.Region] = []

    for uri_region in uri_regions:
        for idx in range(regions_idx, len(st_regions)):
            region = st_regions[idx]

            # later "uri_region" is always even larger so this "idx" is useless since now
            if uri_region.begin() > region.end():
                regions_idx = idx + 1

            if is_regions_intersected(uri_region, region, True):
                uri_regions_intersected.append(uri_region)
                break

    return uri_regions_intersected


def view_last_typing_timestamp_val(view: sublime.View, timestamp_s: Optional[float] = None) -> Optional[float]:
    """
    @brief Set/Get the last timestamp (in sec) when "OUIB_uri_regions" is updated

    @param view        The view
    @param timestamp_s The last timestamp (in sec)

    @return None if the set mode, otherwise the value
    """

    if timestamp_s is None:
        return float(view.settings().get("OUIB_last_update_timestamp", 0))

    view.settings().set("OUIB_last_update_timestamp", timestamp_s)
    return None


def view_is_dirty_val(view: sublime.View, is_dirty: Optional[bool] = None) -> Optional[bool]:
    """
    @brief Set/Get the is_dirty of the current view

    @param view     The view
    @param is_dirty Indicates if dirty

    @return None if the set mode, otherwise the is_dirty
    """

    if is_dirty is None:
        return bool(view.settings().get("OUIB_is_dirty", True))

    view.settings().set("OUIB_is_dirty", is_dirty)
    return None


def is_view_typing(view: sublime.View) -> bool:
    """
    @brief Determine if the view typing.

    @param view The view

    @return `True` if the view is typing, `False` otherwise.
    """

    now_s = get_timestamp()
    last_typing_s = view_last_typing_timestamp_val(view) or 0

    return (now_s - last_typing_s) * 1000 < get_setting("typing_period")


def is_view_too_large(view: sublime.View) -> bool:
    """
    @brief Determine if the view is too large. Note that size will be `0` if the view is loading.

    @param view The view

    @return `True` if the view is too large, `False` otherwise.
    """

    return view.size() > get_setting("large_file_threshold")
