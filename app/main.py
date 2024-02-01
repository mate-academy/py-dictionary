from typing import Hashable, Iterable, Iterator, Any


class Dictionary:

    def __init__(self) -> None:
        self._length = 0
        self._capacity = 8
        self._threshold = int(self._capacity * (2 / 3))
        self._hash_table = [None] * self._capacity

    def _get_initial_index_by_key(self, key: Hashable) -> int:
        return hash(key) % self._capacity

    def _get_actual_index_by_key(self, key: Hashable) -> int:
        index = self._get_initial_index_by_key(key)
        item = self._hash_table[index]

        counter_of_passed_items = 0
        while counter_of_passed_items < self._capacity:
            if item and item[0] == key:
                return index

            counter_of_passed_items += 1
            index = (index + 1) % self._capacity
            item = self._hash_table[index]

        raise KeyError(f"Dictionary doesn't have such key: {key}")

    def __getitem__(self, key: Hashable) -> Any:
        index = self._get_actual_index_by_key(key)
        return self._hash_table[index][2]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._get_initial_index_by_key(key)
        node = (key, hash(key), value)

        while True:
            if not self._hash_table[index]:
                self._hash_table[index] = node
                self._length += 1
                break
            if (
                    self._hash_table[index][0] == key
                    and self._hash_table[index][1] == hash(key)
            ):
                self._hash_table[index] = node
                break

            index = (index + 1) % self._capacity

        if self._length > self._threshold:
            self._resize_hash_table()

    def _resize_hash_table(self) -> None:
        self._capacity *= 2
        self._threshold = int(self._capacity * (2 / 3))
        self._length = 0
        outdated_table = self._hash_table.copy()
        self._hash_table = [None] * self._capacity

        for item in outdated_table:
            if item:
                self.__setitem__(item[0], item[2])

    def __len__(self) -> int:
        return self._length

    def clear(self) -> None:
        self._capacity = 8
        self._hash_table = [None] * self._capacity

    def __delitem__(self, key: Hashable) -> None:
        index = self._get_actual_index_by_key(key)
        self._hash_table[index] = None
        self._length -= 1

    def get(self, key: Hashable, value: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return value

    def pop(self, key: Hashable, *value: Any) -> Any:
        if len(value) > 1:
            raise TypeError(
                f"pop expected at most 2 arguments, got {len(value) + 1}"
            )
        try:
            if existing_value := self.__getitem__(key):
                self.__delitem__(key)
                return existing_value
        except KeyError:
            if value:
                return value[0]
            raise KeyError(f"Dictionary doesn't have such key: {key}")

    def update(self, iterable: Iterable) -> None:
        if isinstance(iterable, dict):
            for key, value in iterable.items():
                self.__setitem__(key, value)
        else:
            try:
                for key, value in iterable:
                    self.__setitem__(key, value)
            except TypeError:
                raise TypeError(
                    "Your iterable object should contain key - value pairs"
                )

    def __iter__(self) -> Iterator:
        return iter(
            [item[0] for item in self._hash_table if item]
        )
