from .types import RegionLike
from typing import Any, Callable, Generator, Iterable, List, Optional, Pattern, Sequence, Tuple, Union
import functools
import sublime


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


def view_find_all_fast(
    view: sublime.View,
    regex_obj: Pattern[str],
    expand_selectors: Iterable[str] = tuple(),
) -> Generator[sublime.Region, None, None]:
    """
    @brief A faster/simpler implementation of View.find_all().

    @param view               the View object
    @param regex_obj          the compiled regex object
    @param expand_selector    the selectors used to expand result regions

    @return A generator for found regions
    """

    if isinstance(expand_selectors, str):
        expand_selectors = (expand_selectors,)

    for m in regex_obj.finditer(view.substr(sublime.Region(0, len(view)))):
        r = sublime.Region(*m.span())
        for selector in expand_selectors:
            if not view.match_selector(r.a, selector):
                continue
            while view.match_selector(r.b, selector):
                r.b += 1
            break
        yield r


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


def region_expand(
    region: RegionLike,
    expansion: Union[int, Tuple[int, int], List[int]],
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

    return (region[0] - expansion[0], region[-1] + expansion[1])


def region_into_tuple_form(region: RegionLike, sort_result: bool = False) -> Tuple[int, int]:
    """
    @brief Convert the "region" into tuple form

    @param region      The region
    @param sort_result Sort the region

    @return the "region" in tuple form
    """

    seq: Sequence[int]

    if isinstance(region, sublime.Region):
        seq = (region.a, region.b)
    elif isinstance(region, int):
        seq = (region, region)
    elif isinstance(region, Iterable):
        seq = tuple(region)[:2]

    if sort_result:
        seq = sorted(seq)

    return (seq[0], seq[-1])


def region_into_st_region_form(region: RegionLike, sort_result: bool = False) -> sublime.Region:
    """
    @brief Convert the "region" into ST's region form

    @param region      The region
    @param sort_result Sort the region

    @return the "region" in ST's region form
    """

    seq: Sequence[int]

    if isinstance(region, int):
        seq = (region, region)
    elif isinstance(region, Iterable):
        seq = tuple(region)[:2]

    if sort_result:
        seq = sorted(seq)

    return sublime.Region(seq[0], seq[-1])


def simplify_intersected_regions(
    regions: Iterable[sublime.Region],
    allow_boundary: bool = False,
) -> List[sublime.Region]:
    """
    @brief Simplify intersected regions by merging them to reduce numbers of regions.

    @param regions        Iterable[sublime.Region] The regions
    @param allow_boundary Treat boundary contact as intersected

    @return Simplified regions
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


def is_regions_intersected(
    region_1: sublime.Region,
    region_2: sublime.Region,
    allow_boundary: bool = False,
) -> bool:
    """
    @brief Check whether two regions are intersected.

    @param region_1       The 1st region
    @param region_2       The 2nd region
    @param allow_boundary Treat boundary contact as intersected

    @return True if intersected, False otherwise.
    """

    return allow_boundary and bool(set(region_1.to_tuple()) & set(region_2.to_tuple())) or region_1.intersects(region_2)


def is_processable_view(view: sublime.View) -> bool:
    return not view.element() and view.is_valid() and not view.is_loading()


def is_transient_view(view: sublime.View) -> bool:
    # @see https://github.com/sublimehq/sublime_text/issues/4444
    # workaround for a transient view have no window right after it's loaded
    if not (window := view.window()):
        return True
    # @see https://forum.sublimetext.com/t/is-view-transient-preview-method/3247/2
    return view == window.transient_view_in_group(window.active_group())
