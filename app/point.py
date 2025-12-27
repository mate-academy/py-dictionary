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
        # Измените реализацию хэша для отладки кода.
        # Например, вы можете вернуть self.x + self.y как хэш.
        # Это НЕ является рекомендуемой практикой, но вы сможете предсказать
        # значение хэша по координатам точки и её индексу
        # в хэш-таблице.
        return hash((self.x, self.y))

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y
