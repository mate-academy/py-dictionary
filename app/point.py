from typing import Any


class Point:
    def __init__(self, x: float, y: float) -> None:
        self._x = x
        self._y = y

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash(self.x) ^ hash(self.y)

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y
