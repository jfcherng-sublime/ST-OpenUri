from __future__ import annotations

from typing import TypedDict

import sublime

type RegionLike = (
    sublime.Region
    | int  # point
    | list[int]  # region in list form
    | tuple[int, int]  # region in tuple form
)


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
