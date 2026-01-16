from typing import Any


class Point:
    def __init__(self, x: float, y: float) -> None:
        self._x: float = x
        self._y: float = y

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        # Simplified hash for debugging: predictable and easy to trace
        return int(self.x + self.y)

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    def __repr__(self) -> str:
        return f"Point(x={self.x}, y={self.y})"
