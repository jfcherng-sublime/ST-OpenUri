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


class ImageDict(TypedDict):
    base64: str
    bytes: bytes
    ext: str
    mime: str
    path: str
    ratio_wh: float
    size: Tuple[int, int]


class UriSource(enum.Enum):
    CURSORS = enum.auto()
    FILE = enum.auto()
