from dataclasses import dataclass
from typing import Any, Iterable, Hashable, Iterator


class DeletedNode:
    pass


_MISSING = object()


@dataclass
class Node:
    key: Hashable
    value: Any
    hashcode: int


class Dictionary:
    def __init__(self, *args: Iterable, **kwargs: Any) -> None:
        self.capacity = 8
        self.hash_array: list[int] = [-1] * self.capacity
        self.ordered_data = []
        self.count = 0
        self.update(*args, **kwargs)

    def __len__(self) -> int:
        return self.count

    def _resize_hash_array(self) -> None:
        self.capacity *= 2
        old_ordered_data = self.ordered_data
        self.clear()
        for node in old_ordered_data:
            if not isinstance(node, DeletedNode):
                self[node.key] = node.value

    def __setitem__(self, key: Any, value: Any) -> None:
        _hash = hash(key)
        if self.__len__() >= int(self.capacity * 2 / 3):
            self._resize_hash_array()

        _index = _hash % self.capacity
        while True:
            current_node_index = self.hash_array[_index]
            if current_node_index < 0:
                self.hash_array[_index] = len(self.ordered_data)
                self.ordered_data.append(Node(key=key, value=value,
                                              hashcode=_hash))
                self.count += 1
                break
            current_node = self.ordered_data[current_node_index]
            if current_node.hashcode == _hash and current_node.key == key:
                self.ordered_data[current_node_index] = (
                    Node(key=key, value=value, hashcode=_hash)
                )
                break
            _index += 1
            if _index == self.capacity:
                _index = 0

    def __getitem__(self, item: Any) -> Any:
        _hash = hash(item)
        _index = _hash % self.capacity
        while True:
            current_node_index = self.hash_array[_index]
            if current_node_index == -1:
                raise KeyError(f"Key not found: {item}")
            if current_node_index != -2:
                current_node = self.ordered_data[current_node_index]
                if current_node.hashcode == _hash and current_node.key == item:
                    return current_node.value
            _index += 1
            if _index == self.capacity:
                _index = 0

    def clear(self) -> None:
        self.count = 0
        self.hash_array = [-1] * self.capacity
        self.ordered_data = []

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def __delitem__(self, key: Any) -> None:
        _hash = hash(key)
        _index = _hash % self.capacity
        while True:
            current_node_index = self.hash_array[_index]
            if current_node_index < 0:
                raise KeyError(f"Key not found: {key}")
            if current_node_index != -2:
                current_node = self.ordered_data[current_node_index]
                if current_node.hashcode == _hash and current_node.key == key:
                    self.hash_array[_index] = -2
                    self.ordered_data[current_node_index] = DeletedNode()
                    self.count -= 1
                    return
            _index += 1
            if _index == self.capacity:
                _index = 0

    def __iter__(self) -> Iterator[Any]:
        for node in self.ordered_data:
            if not isinstance(node, DeletedNode):
                yield node.key

    def pop(self, key: Any, default: Any = _MISSING) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default is _MISSING:
                raise
            else:
                return default

    def update(self, *args: Iterable, **kwargs: Any) -> None:
        if args:
            args = args[0]
            if isinstance(args, Dictionary):
                for key in args:
                    self[key] = args[key]
            elif isinstance(args, list | tuple):
                for key, value in args:
                    self[key] = value
            else:
                raise TypeError(f"{args}: unsupported type")
        if kwargs:
            for key, value in kwargs.items():
                self[key] = value
