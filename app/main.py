from typing import Any

class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.hash = hash(key)
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self.data = []

    def __setitem__(self, key: Any, value: Any) -> None:
        for node in self.data:
            if node.key == key:
                node.value = value
                return
        self.data.append(Node(key, value))

    def __getitem__(self, key: Any) -> Any:
        for node in self.data:
            if node.key == key:
                return node.value
        raise KeyError(f"Key {key} not found")

    def __len__(self):
        return len(self.data)
