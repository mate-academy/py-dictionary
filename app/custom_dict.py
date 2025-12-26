from typing import Any, Hashable
from math import ceil


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value


class CustomDict:
    _no_value = object()
    _deleted_marker = object()

    def __init__(self) -> None:
        self.capacity: int = 8
        self.dictionary: list[Node | object | None] = [None] * self.capacity
        self.load_factor: float = 2 / 3
        self._used_cells_counter: int = 0

    @property
    def threshold(self) -> int:
        return ceil(self.capacity * self.load_factor)

    def __len__(self) -> int:
        return self._used_cells_counter

    def __setitem__(self, key: Hashable, value: Any) -> None:
        new_node = Node(key, value)
        index = self._probe(key)

        if index is None:
            index = hash(key) % self.capacity
            for i in range(self.capacity):
                probe_index = (index + i) % self.capacity
                if self.dictionary[probe_index] in {
                    None, self._deleted_marker
                }:
                    self.dictionary[probe_index] = new_node
                    self._used_cells_counter += 1
                    break
        else:
            self.dictionary[index].value = value

        if self._used_cells_counter >= self.threshold:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self._probe(key)
        if index is None:
            raise KeyError(f"Key {key} is not found in the dictionary")
        return self.dictionary[index].value

    def __delitem__(self, key: Hashable) -> None:
        index = self._probe(key)
        if index is None:
            raise KeyError(f"Key {key} is not present in the dictionary."
                           f" Unable to delete.")
        self.dictionary[index] = self._deleted_marker
        self._used_cells_counter -= 1

    def pop(self, key: Hashable, default: Any = _no_value) -> Any:
        index = self._probe(key)
        if index is None:
            if default is self._no_value:
                raise KeyError(f"Key {key} is not present in the dictionary."
                               f" Unable to pop.")
            return default

        value = self.dictionary[index].value
        self.dictionary[index] = self._deleted_marker
        self._used_cells_counter -= 1
        return value

    def _resize(self) -> None:
        old_dict = self.dictionary
        self.capacity *= 2
        self.dictionary = [None] * self.capacity
        self._used_cells_counter = 0

        for node in old_dict:
            if isinstance(node, Node):
                self.__setitem__(node.key, node.value)

    def _probe(self, key: Hashable) -> int | None:
        index = hash(key) % self.capacity
        for i in range(self.capacity):
            probe_index = (index + i) % self.capacity
            if self.dictionary[probe_index] is None:
                return None
            if (
                    self.dictionary[probe_index] is not self._deleted_marker
                    and self.dictionary[probe_index].key == key
            ):
                return probe_index
        return None
