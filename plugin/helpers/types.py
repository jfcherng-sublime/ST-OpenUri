from __future__ import annotations

# __future__ must be the first import
from typing import List, Tuple, TypedDict, Union
import enum
import sublime

RegionLike = Union[
    sublime.Region,
    # point
    int,
    # region in list form
    List[int],
    # region in tuple form
    Tuple[int, int],
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
    size: Tuple[int, int]


class UriSource(enum.Enum):
    CONTEXT_MENU = enum.auto()
    CURSORS = enum.auto()
    FILE = enum.auto()
    NONE = enum.auto()
