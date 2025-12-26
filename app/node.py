from typing import Any, Hashable


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        try:
            self.hash = hash(key)
        except TypeError:
            raise TypeError(f"Unhashable key: {key} ({type(key).__name__})")

        self.key = key
        self.value = value
