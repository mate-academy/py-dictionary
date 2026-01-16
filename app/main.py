from __future__ import annotations
from typing import Any, Hashable


class Dictionary:
    _initial_size = 8
    _load_factor = 0.75
    _resize_factor = 2

    def __init__(
            self,
            initial_content: list[tuple[Hashable, Any]] = None
    ) -> None:
        self._size = Dictionary._initial_size
        self._load = 0
        self._table = [DictionaryNode() for _ in range(self._size)]

        self.update(initial_content)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        node = self._get_node(key)

        if node.is_empty():
            self._load += 1
        node.update(key, value)

        if self._load / self._size >= Dictionary._load_factor:
            self._resize()

    def __getitem__(self, item: Hashable) -> Any:
        node = self._get_node(item)
        if node.is_empty():
            raise KeyError(f"{item} key is not found.")
        return node.value

    def __len__(self) -> int:
        return self._load

    def __delitem__(self, item: Hashable) -> None:
        node = self._get_node(item)

        if not node.is_empty():
            node.clear()

    def __str__(self) -> str:
        return ", ".join([f"{key}: {value}" for key, value in self.items()])

    def __iter__(self) -> iter:
        return iter(self.keys())

    def _get_node(self, key: Hashable) -> "DictionaryNode":
        index = hash(key) % self._size
        node = self._table[index]

        while not node.is_empty() and node.key != key:
            if node.link is None or index != hash(key) % self._size:
                index = (index + 1) % self._size
                node = self._table[index]
            else:
                node = self._table[node.link]

        return node

    def update(
            self,
            dictionary: "Dictionary" | list | None
    ) -> None:
        if isinstance(dictionary, Dictionary):
            items = dictionary.items()
        elif isinstance(dictionary, list):
            items = dictionary
        else:
            items = []

        for key, value in items:
            self.__setitem__(key, value)

    def clear(self) -> None:
        self._load = 0
        self._table = [DictionaryNode() for _ in range(self._size)]

    def items(self) -> list[tuple]:
        return [(node.key, node.value) for node in self._table
                if not node.is_empty()]

    def keys(self) -> list[tuple]:
        return [node.key for node in self._table if not node.is_empty()]

    def values(self) -> list[tuple]:
        return [node.value for node in self._table if not node.is_empty()]

    def _resize(self) -> None:
        items = self.items()
        self._size *= Dictionary._resize_factor
        self.clear()

        for key, value in items:
            self.__setitem__(key, value)

    def get(self, key: Hashable) -> Any | None:
        try:
            return self.__getitem__(key)
        except KeyError:
            return None

    def pop(self, key: Hashable) -> Any | None:
        value = self.get(key)
        self.__delitem__(key)

        return value


class DictionaryNode:
    def __init__(self) -> None:
        self.key = None
        self.value = None
        self.key_hash = None
        self.link = None

    def __repr__(self) -> str:
        if not self.is_empty():
            string = f"{self.key}: {self.value}, hash={self.key_hash}"

            if self.link is not None:
                string += f", link={self.link}"
        else:
            string = "empty"

        return string

    def update(self, key: Hashable | None, value: Any) -> None:
        self.key = key
        self.value = value
        self.key_hash = None if self.is_empty() else hash(key)

    def clear(self) -> None:
        self.update(None, None)

    def is_empty(self) -> bool:
        return self.key is None
