import itertools
import time
from typing import Any, Callable, Generator, Iterable, List, Optional, Pattern, Sequence, Tuple, Union, cast, overload

import sublime

from .constants import ST_SUPPORT_EXPAND_TO_SCOPE
from .types import RegionLike, T_AnyCallable


def get_timestamp() -> float:
    return time.time()


def list_all_views(*, include_transient: bool = False) -> Generator[sublime.View, None, None]:
    for window in sublime.windows():
        yield from window.views(include_transient=include_transient)


def list_background_views() -> Generator[sublime.View, None, None]:
    foreground_views = set(list_foreground_views())
    for view in list_all_views(include_transient=True):
        if view not in foreground_views:
            yield view


def list_foreground_views() -> Generator[sublime.View, None, None]:
    for window in sublime.windows():
        for group_idx in range(window.num_groups()):
            if view := window.active_view_in_group(group_idx):
                yield view


def simple_decorator(decorator: Callable) -> Callable[[T_AnyCallable], T_AnyCallable]:
    """A decorator that turns a function into a decorator."""

    def wrapper(decoratee: T_AnyCallable) -> T_AnyCallable:
        def wrapped(*args, **kwargs) -> Any:
            return decorator(decoratee(*args, **kwargs))

        return cast(T_AnyCallable, wrapped)

    return wrapper


def dotted_get(var: Any, dotted: str, default: Optional[Any] = None) -> Any:
    """
    @brief Get the value from the variable with dotted notation.

    @param var     The variable
    @param dotted  The dotted
    @param default The default

    @return The value or the default if dotted not found
    """
    keys = dotted.split(".")

    try:
        for key in keys:
            if isinstance(var, (dict, sublime.Settings)):
                var = var.get(key)
            elif isinstance(var, (list, tuple, bytes, bytearray)):
                var = var[int(key)]
            else:
                var = getattr(var, key)

        return var
    except Exception:
        return default


def dotted_set(var: Any, dotted: str, value: Any) -> None:
    """
    @brief Set the value for the variable with dotted notation.

    @param var     The variable
    @param dotted  The dotted
    @param default The default
    """
    keys = dotted.split(".")
    last_key = keys.pop()

    for key in keys:
        if isinstance(var, (dict, sublime.Settings)):
            var = var.get(key)
        elif isinstance(var, (list, tuple, bytes, bytearray)):
            var = var[int(key)]
        else:
            var = getattr(var, key)

    if isinstance(var, (dict, sublime.Settings)):
        var[last_key] = value  # type: ignore
    elif isinstance(var, (list, tuple, bytes, bytearray)):
        var[int(last_key)] = value  # type: ignore
    else:
        setattr(var, last_key, value)


def view_find_all(
    view: sublime.View,
    regex_obj: Pattern[str],
    expand_selectors: Iterable[str] = tuple(),
) -> Generator[sublime.Region, None, None]:
    """
    @brief Find all content matching the regex and expand found regions with selectors.

    @param view               the View object
    @param regex_obj          the compiled regex object
    @param expand_selector    the selectors used to expand found regions

    @return A generator for found regions
    """

    def expand(region: sublime.Region) -> sublime.Region:
        if ST_SUPPORT_EXPAND_TO_SCOPE:
            return next(
                filter(None, (view.expand_to_scope(region.a, selector) for selector in expand_selectors)),
                region,
            )

        for selector in expand_selectors:
            if not view.match_selector(region.a, selector):
                continue
            while view.match_selector(region.b, selector):
                region.b += 1
            break
        return region

    if isinstance(expand_selectors, str):
        expand_selectors = (expand_selectors,)

    for m in regex_obj.finditer(view.substr(sublime.Region(0, len(view)))):
        yield expand(sublime.Region(*m.span()))


@overload
def view_last_typing_timestamp_val(view: sublime.View) -> float:
    ...


@overload
def view_last_typing_timestamp_val(view: sublime.View, timestamp_s: float) -> None:
    ...


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


@overload
def view_is_dirty_val(view: sublime.View) -> bool:
    ...


@overload
def view_is_dirty_val(view: sublime.View, is_dirty: bool) -> None:
    ...


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


@overload
def region_shift(region: sublime.Region, shift: int) -> sublime.Region:
    ...


@overload
def region_shift(region: Union[int, List[int], Tuple[int, int]], shift: int) -> Tuple[int, int]:
    ...


def region_shift(region: RegionLike, shift: int) -> Union[Tuple[int, int], sublime.Region]:
    """
    @brief Shift the region by given amount.

    @param region The region
    @param shift  The shift

    @return the shifted region
    """
    if isinstance(region, int):
        return (region + shift, region + shift)

    if isinstance(region, sublime.Region):
        return sublime.Region(region.a + shift, region.b + shift)

    return (region[0] + shift, region[-1] + shift)


@overload
def region_expand(
    region: sublime.Region,
    expansion: Union[int, List[int], Tuple[int, int]],
) -> sublime.Region:
    ...


@overload
def region_expand(
    region: Union[int, List[int], Tuple[int, int]],
    expansion: Union[int, List[int], Tuple[int, int]],
) -> Tuple[int, int]:
    ...


def region_expand(
    region: RegionLike,
    expansion: Union[int, List[int], Tuple[int, int]],
) -> Union[Tuple[int, int], sublime.Region]:
    """
    @brief Expand the region by given amount.

    @param region    The region
    @param expansion The amount of left/right expansion

    @return the expanded region
    """
    if isinstance(expansion, int):
        expansion = (expansion, expansion)

    if isinstance(region, int):
        return (region - expansion[0], region + expansion[1])

    if isinstance(region, sublime.Region):
        return sublime.Region(region.a - expansion[0], region.b + expansion[1])

    return (region[0] - expansion[0], region[-1] + expansion[-1])


def convert_to_region_tuple(region: RegionLike, sort: bool = False) -> Tuple[int, int]:
    """
    @brief Convert the "region" into its tuple form

    @param region The region
    @param sort   Sort the region

    @return the "region" in tuple form
    """
    seq: Sequence[int]

    if isinstance(region, sublime.Region):
        seq = region.to_tuple()
    elif isinstance(region, int):
        seq = (region, region)
    elif isinstance(region, Iterable):
        seq = tuple(itertools.islice(region, 2))

    if sort:
        seq = sorted(seq)

    return (seq[0], seq[-1])


def convert_to_st_region(region: RegionLike, sort: bool = False) -> sublime.Region:
    """
    @brief Convert the "region" into its ST region form

    @param region The region
    @param sort   Sort the region

    @return the "region" in ST's region form
    """
    return sublime.Region(*convert_to_region_tuple(region, sort))


def merge_regions(regions: Iterable[sublime.Region], allow_boundary: bool = False) -> List[sublime.Region]:
    """
    @brief Merge intersected regions to reduce numbers of regions.

    @param regions        The regions, whose `region.a <= region.b`
    @param allow_boundary Treat boundary contact as intersected

    @return Merged regions
    """
    merged_regions: List[sublime.Region] = []
    for region in sorted(regions):
        if not merged_regions:
            merged_regions.append(region)
            continue

        if is_regions_intersected(merged_regions[-1], region, allow_boundary):
            merged_regions[-1].b = region.b
        else:
            merged_regions.append(region)

    return merged_regions


def is_regions_intersected(region1: sublime.Region, region2: sublime.Region, allow_boundary: bool = False) -> bool:
    """
    @brief Determinates whether two regions are intersected.

    @param region1        The 1st region
    @param region2        The 2nd region
    @param allow_boundary Treat boundary contact as intersected

    @return True if intersected, False otherwise.
    """
    return region1.intersects(region2) or bool(allow_boundary and {*region1.to_tuple()} & {*region2.to_tuple()})


def is_processable_view(view: sublime.View) -> bool:
    return view.is_valid() and not view.is_loading() and not view.element()


def is_transient_view(view: sublime.View) -> bool:
    return sheet.is_transient() if view.is_valid() and (sheet := view.sheet()) else False
