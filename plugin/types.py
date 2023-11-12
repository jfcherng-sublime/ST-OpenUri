from __future__ import annotations

from collections.abc import Callable
from typing import Any, List, Tuple, TypedDict, TypeVar, Union

import sublime

T_AnyCallable = TypeVar("T_AnyCallable", bound=Callable[..., Any])

RegionLike = Union[
    sublime.Region,
    int,  # point
    List[int],  # region in list form
    Tuple[int, int],  # region in tuple form
]


class EventDict(TypedDict):
    x: float
    y: float
    modifier_keys: EventModifierKeysDict


class EventModifierKeysDict(TypedDict, total=False):
    primary: bool
    ctrl: bool
    alt: bool
    altgr: bool
    shift: bool
    super: bool


class ImageDict(TypedDict):
    base64: str
    bytes: bytes
    ext: str
    mime: str
    path: str
    ratio_wh: float
    size: tuple[int, int]
