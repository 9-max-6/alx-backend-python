#!/usr/bin/env python3
"""module: function: element_length
"""
from typing import Iterable, Tuple, Sequence, List


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """function to compute the length of a list of sequences.
    """
    return [(i, len(i)) for i in lst]