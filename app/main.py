from typing import Any, Iterable


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.hash = hash(key)
        self.value = value


class Dictionary:
    def __init__(self, *args: Iterable, **kwargs: Any) -> None:
        self.capacity: int = 8
        self.hash_array: list[Node | None] = [None] * self.capacity
        self.count: int = 0
        if args:
            if not isinstance(args[0], list | tuple):
                raise TypeError(f"{args}: should be list of tuple")
            for key, value in args[0]:
                self[key] = value
        if kwargs:
            for key, value in kwargs.items():
                self[key] = value

    def __len__(self) -> int:
        return self.count

    def _resize_hash_array(self) -> None:
        old_hash_array = self.hash_array
        self.capacity *= 2
        self.hash_array = [None] * self.capacity
        self.count = 0
        for node in old_hash_array:
            if node:
                self[node.key] = node.value

    def __setitem__(self, key: Any, value: Any) -> None:
        _hash = hash(key)
        if self.__len__() == int(self.capacity * 2 / 3):
            self._resize_hash_array()

        _index = _hash % self.capacity
        while True:
            if self.hash_array[_index] is None:
                self.hash_array[_index] = Node(key=key, value=value)
                self.count += 1
                break
            if self.hash_array[_index].key == key:
                self.hash_array[_index] = Node(key=key, value=value)
                break
            _index += 1
            if _index == self.capacity:
                _index = 0

    def __getitem__(self, item: Any) -> Any:
        _hash = hash(item)
        _index = _hash % self.capacity
        while True:
            if self.hash_array[_index] is None:
                raise KeyError(f"Key not found: {item}")
            if self.hash_array[_index].key == item:
                return self.hash_array[_index].value
            _index += 1
            if _index == self.capacity:
                _index = 0

    def clear(self) -> None:
        self.count = 0
        self.hash_array = [None] * self.capacity

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default
