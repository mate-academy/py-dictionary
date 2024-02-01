from typing import Hashable, Any


class Node:
    def __init__(self, hashed: int, key: Hashable, value: Any) -> None:
        self.hashed = hashed
        self.key = key
        self.value = value

    def __repr__(self) -> str:
        return f"({self.hashed}, {self.key}, {self.value})"
