from typing import List, Tuple, Union
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
