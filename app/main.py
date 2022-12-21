from __future__ import annotations
from typing import Any, Union, Tuple, Iterable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.resize_multiplier = 2

        self.length = 0
        self.resize_threshold = None
        self._update_threshold()
        self.hash_table: list = [None] * self.capacity

    def __len__(self) -> int:
        return self.length

    def _get_hash_and_index(
        self,
        key: Union[bool, int, float, str, tuple]
    ) -> Tuple[int, int]:
        hash_of_key = key.__hash__()
        index_of_item = hash_of_key % self.capacity

        return (hash_of_key, index_of_item)

    def __setitem__(
        self,
        key: Union[bool, int, float, str, tuple],
        value: Any
    ) -> None:
        hash_of_key, index_of_item = self._get_hash_and_index(key)

        node = [key, hash_of_key, value]

        while True:
            current_item = self.hash_table[index_of_item]

            if current_item is None:
                self.length += 1

            if current_item is None or current_item[0] == node[0]:
                self.hash_table[index_of_item] = node

                break

            index_of_item = (index_of_item + 1) % self.capacity

        if (self.length > self.resize_threshold):
            self.resize()

    def __getitem__(
        self,
        key: Union[bool, int, float, str, tuple]
    ) -> Any:
        hash_of_key, index_of_item = self._get_hash_and_index(key)

        while True:
            node = self.hash_table[index_of_item]

            if node is None:
                raise KeyError

            if node[0] == key:
                return node[2]
            else:
                index_of_item = (index_of_item + 1) % self.capacity

    def resize(self) -> None:
        self.capacity *= self.resize_multiplier

        old_table = self.hash_table
        self.length = 0
        self.hash_table = [None] * self.capacity

        self._update_threshold()

        for i in range(len(old_table)):
            if old_table[i] is not None:
                self.__setitem__(old_table[i][0], old_table[i][2])

    def _update_threshold(self) -> None:
        self.resize_threshold = self.load_factor * self.capacity

    def clear(self) -> None:
        self.hash_table: list = [None] * self.capacity

    def get(
        self,
        key: Union[bool, int, float, str, tuple],
        default_value: Any = None
    ) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default_value

    def update(self, values_for_dict: Iterable) -> None:
        try:
            for key in values_for_dict:
                self.__setitem__(key, values_for_dict[key])
        except TypeError:
            for item in values_for_dict:
                self.__setitem__(item[0], item[1])

    def __iter__(self) -> Dictionary:
        self.current_index = 0
        return self

    def __next__(self) -> Any:
        while True:
            if self.current_index > self.capacity - 1:
                raise StopIteration

            item = self.hash_table[self.current_index]

            self.current_index += 1

            if item is not None:
                return item[0]

    def __delitem__(
        self,
        key: Union[bool, int, float, str, tuple]
    ) -> None:
        index_of_item = self._get_hash_and_index(key)[1]

        while True:
            node = self.hash_table[index_of_item]

            if node is None:
                raise KeyError

            if node[0] == key:
                self.hash_table[index_of_item] = None

                self.length -= 1

                self._move_colliding_nodes(index_of_item)

                break
            else:
                index_of_item = (index_of_item + 1) % self.capacity

    def _move_colliding_nodes(
        self,
        index_of_item: int
    ) -> None:
        last_index = index_of_item
        while True:
            index_of_item = (index_of_item + 1) % self.capacity

            node = self.hash_table[index_of_item]

            if node is None:
                break

            true_index_of_item = self._get_hash_and_index(node[0])[1]

            distance_to_last = index_of_item - last_index
            distance_to_true = index_of_item - true_index_of_item

            if distance_to_last < 0:
                distance_to_last += self.capacity

            if distance_to_true < 0:
                distance_to_true += self.capacity

            if (
                true_index_of_item != index_of_item
                and distance_to_true >= distance_to_last
            ):
                self.hash_table[last_index] = self.hash_table[index_of_item]
                self.hash_table[index_of_item] = None
                last_index = index_of_item

    def pop(
        self,
        key: Union[bool, int, float, str, tuple],
        default_value: Any = None
    ) -> Any:
        try:
            value = self.__getitem__(key)
            self.__delitem__(key)
            return value
        except KeyError:
            if default_value is not None:
                return default_value
            else:
                raise KeyError
