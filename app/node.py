from typing import Any


class Node:
    def __init__(self, key: int, value: Any) -> None:
        try:
            self.hash_key = hash(key)
        except TypeError:
            raise TypeError("Key must be hashable")
        self.key = key
        self.value = value
