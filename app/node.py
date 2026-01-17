from typing import Any, Hashable


class Node:
    def __init__(
            self,
            key: Hashable,
            hash_custom: int,
            value: Any
    ) -> None:
        self.key = key
        self.hash = hash_custom
        self.value = value

    def __repr__(self) -> str:
        return f"{self.key}: {self.value}"
