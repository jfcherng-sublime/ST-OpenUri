import functools
import sublime
from typing import Any, Callable, Iterable, List, Optional, Pattern, Union
from .st_types import RegionLike


def simple_decorator(decorator: Callable) -> Callable:
    """
    @brief A decorator that turns a function into a decorator.
    """

    @functools.wraps(decorator)
    def outer_wrapper(decoratee: Callable) -> Callable:
        @functools.wraps(decoratee)
        def wrapper(*args, **kwargs) -> Any:
            return decorator(decoratee(*args, **kwargs))

        return wrapper

    return outer_wrapper


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


def view_find_all_fast(view: sublime.View, regex_obj: Pattern) -> List[sublime.Region]:
    """
    @brief A faster/simpler implementation of View.find_all().

    @param view             the View object
    @param regex_obj        the compiled regex object

    @return Found regions
    """

    return [
        sublime.Region(*m.span())
        for m in regex_obj.finditer(view.substr(sublime.Region(0, view.size())))
    ]


def region_shift(region: RegionLike, shift: int) -> RegionLike:
    """
    @brief Shift the region by given amount.

    @param region The region
    @param shift  The shift

    @return the shifted region
    """

    if isinstance(region, (int, float)):
        return region + shift

    if isinstance(region, sublime.Region):
        return sublime.Region(region.a + shift, region.b + shift)

    return [region[0] + shift, region[-1] + shift]


def region_expand(region: RegionLike, expansion: Union[int, List[int]]) -> RegionLike:
    """
    @brief Expand the region by given amount.

    @param region    The region
    @param expansion The amount of left/right expansion

    @return the expanded region
    """

    if isinstance(expansion, (int, float)):
        expansion = [int(expansion)] * 2

    if len(expansion) == 0:
        raise ValueError("Invalid expansion: {}".format(expansion))

    if len(expansion) == 1:
        # do not modify the input variable by "expansion *= 2"
        expansion = [expansion[0]] * 2

    if isinstance(region, (int, float)):
        return [region - expansion[0], region + expansion[1]]

    if isinstance(region, sublime.Region):
        return sublime.Region(region.begin() - expansion[0], region.end() + expansion[1])

    # fmt: off
    return [
        min(region[0], region[-1]) - expansion[0],
        max(region[0], region[-1]) + expansion[1],
    ]
    # fmt: on


def region_into_list_form(region: RegionLike, sort_result: bool = False) -> List[int]:
    """
    @brief Convert the "region" into list form

    @param region      The region
    @param sort_result Sort the region

    @return the "region" in list form
    """

    if isinstance(region, sublime.Region):
        region = [region.a, region.b]
    elif isinstance(region, (int, float)):
        region = [int(region)] * 2
    elif isinstance(region, Iterable) and not isinstance(region, list):
        region = list(region)

    assert isinstance(region, list)

    if not region:
        raise ValueError("region must not be empty.")

    if len(region) > 0:
        region = [region[0], region[-1]]

    return sorted(region) if sort_result else region


def region_into_st_region_form(region: RegionLike, sort_result: bool = False) -> sublime.Region:
    """
    @brief Convert the "region" into ST's region form

    @param region      The region
    @param sort_result Sort the region

    @return the "region" in ST's region form
    """

    if isinstance(region, (int, float)):
        region = [int(region)] * 2
    elif isinstance(region, Iterable) and not isinstance(region, list):
        region = list(region)

    if isinstance(region, list) and not region:
        raise ValueError("region must not be empty.")

    if not isinstance(region, sublime.Region):
        region = sublime.Region(region[0], region[-1])

    return sublime.Region(region.begin(), region.end()) if sort_result else region


def simplify_intersected_regions(
    regions: Iterable[sublime.Region], allow_boundary: bool = False
) -> List[sublime.Region]:
    """
    @brief Simplify intersected regions by merging them to reduce numbers of regions.

    @param regions        Iterable[sublime.Region] The regions
    @param allow_boundary Treat boundary contact as intersected

    @return Simplified regions
    """

    merged_regions = []  #  type: List[sublime.Region]
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


def is_view_normal_ready(view: Optional[sublime.View]) -> bool:
    return bool(view and not view.settings().get("is_widget") and not view.is_loading())
