from typing import Any


class Node:
    def __init__(self, key: Any, hash_code: int, value: Any) -> None:
        self.key: Any = key
        self.hash_code: int = hash_code
        self.value: Any = value
