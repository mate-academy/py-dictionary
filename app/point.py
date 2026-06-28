from random import uniform, randint, seed
from typing import Any

from app.main import Dictionary


class Point:
    def __init__(self, x: float, y: float) -> None:
        self._x = x
        self._y = y

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        # Change the implementation of the hash to debug your code.
        # For example, you can return self.x + self.y as a hash
        # which is NOT a best practice, but you will be able to predict
        # a hash value by coordinates of the point and its index
        # in the hashtable as well
        radius = (self._x ** 2 + self._y ** 2) ** 0.5
        if radius % 1 == 0:
            return int(radius)
        return int(str(radius).replace(".", ""))

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    def __repr__(self) -> str:
        return f"({self._x}, {self._y})"


if __name__ == "__main__":
    seed(2.5)
    dictionary = Dictionary()
    pairs = [
        (
            Point(round(uniform(0, 10), 2), round(uniform(0, 10), 2)),
            randint(0, 10)
        )
        for _ in range(8)
    ]
    print(pairs)
    dictionary.update(*pairs[:5])
    print(dictionary)
    print(dictionary[Point(7.57, 6.06)])
    print(dictionary.get(Point(8.57, 6.06), "key not found"))
    print(dictionary.pop(Point(8.57, 6.06)))
    print(dictionary.pop(Point(7.57, 6.06)))
    for item in dictionary:
        print(item)
    dictionary.update(*pairs[5:])
    print(dictionary)
