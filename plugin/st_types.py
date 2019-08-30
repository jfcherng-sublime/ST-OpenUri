from typing import List, Tuple, Union

RegionLike = Union[
    # point
    int,
    # region in list form
    List[int],
    # region in tuple form
    Tuple[int, int],
]
