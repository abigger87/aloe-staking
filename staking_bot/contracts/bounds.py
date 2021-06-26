'''
Aloe Capital LLC
06-12-2021
MIT License
'''

from typing import NamedTuple

class Bounds(NamedTuple):
    lower: int
    upper: int
    are_inverted: bool


def inverted(bounds: Bounds) -> Bounds:
    lower = (2.0 ** 32) / float(bounds.upper)
    upper = (2.0 ** 32) / float(bounds.lower)
    return Bounds(int(lower), int(upper), not bounds.are_inverted)
