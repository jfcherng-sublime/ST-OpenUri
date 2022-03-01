# This file is maintained on https://github.com/jfcherng-sublime/ST-API-stubs

from __future__ import annotations

# __future__ must be the first import
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Sequence,
    Tuple,
    TypedDict,
    TypeVar,
    Union,
)
import sublime

# ----- #
# types #
# ----- #

T = TypeVar("T")
AnyCallable = TypeVar("AnyCallable", bound=Callable[..., Any])
ExpandableVar = TypeVar("ExpandableVar", bound=Union[None, bool, int, float, str, Dict, List, Tuple])

Callback0 = Callable[[], Any]
Callback1 = Callable[[T], Any]

Point = int
Dip = float
Str = str  # alias in case we have a variable named as "str"

Completion = Union[str, Sequence[str], Tuple[str, str], sublime.CompletionItem]
CompletionKind = Tuple[int, str, str]
CompletionNormalized = Tuple[
    str,  # trigger
    str,  # annotation
    str,  # details
    str,  # completion
    str,  # kind_name
    int,  # icon letter (Unicode code point, decimal form)
    int,  # completion_format
    int,  # flags
    int,  # kind
]

Location = Tuple[str, str, Tuple[int, int]]
Vector = Tuple[Dip, Dip]


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


class Layout(TypedDict):
    cols: List[float]
    rows: List[float]
    cells: List[List[int]]
