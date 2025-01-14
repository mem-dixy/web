""""""

from celestine.typed import (
    TZ2,
    TZ3,
    K,
    N,
    Z,
)


class Rect:
    """"""


class Surface:
    """"""

    color: TZ3
    dest: TZ2
    height: Z
    size: TZ2
    source: K
    width: Z

    def blit(self, source: K, dest: TZ2) -> Rect:
        """"""
        self.source = source
        self.dest = dest
        return Rect()

    def convert_alpha(self) -> K:
        """"""
        return self

    def fill(self, color: TZ3) -> Rect:
        """"""
        self.color = color
        return Rect()

    def get_height(self) -> Z:
        """"""
        return self.height

    def get_width(self) -> Z:
        """"""
        return self.width

    def __init__(self, size: TZ2) -> N:
        """"""
        self.color = (0, 0, 0)
        self.dest = (0, 0)
        self.height = 0
        self.size = size
        self.source = self
        self.width = 0
