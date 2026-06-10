from typing import Hashable, Any, Iterator


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.threshold = 5
        self.key_table: list = [None] * 8
        self.hash_table: list = [None] * 8
        self.value_table: list = [None] * 8

    @staticmethod
    def _find_index(
            key: Hashable,
            key_hash: int,
            capacity: int,
            key_table: list,
            hash_table: list
    ) -> int:
        index = key_hash % capacity
        is_index_found = False
        while not is_index_found:
            if hash_table[index] is None:
                is_index_found = True
            elif key_table[index] == key and hash_table[index] == key_hash:
                is_index_found = True
            else:
                index = (index + 1) % capacity
        return index

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_key_table: list = [None] * new_capacity
        new_hash_table: list = [None] * new_capacity
        new_value_table: list = [None] * new_capacity
        for old_index in range(self.capacity):
            if self.hash_table[old_index] is not None:
                key_hash = self.hash_table[old_index]
                key = self.key_table[old_index]
                value = self.value_table[old_index]
                new_index = self._find_index(
                    key, key_hash, new_capacity, new_key_table, new_hash_table
                )
                new_key_table[new_index] = key
                new_hash_table[new_index] = key_hash
                new_value_table[new_index] = value
        self.key_table = new_key_table
        self.hash_table = new_hash_table
        self.value_table = new_value_table
        self.capacity = new_capacity
        self.threshold = round(new_capacity * 2 / 3)

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = hash(key)
        index = self._find_index(
            key, key_hash, self.capacity, self.key_table, self.hash_table
        )
        if self.hash_table[index] is None:
            raise KeyError
        return self.value_table[index]

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            value = self.__getitem__(key)
        except KeyError:
            return default
        return value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length == self.threshold:
            self._resize()

        key_hash = hash(key)
        index = self._find_index(
            key, key_hash, self.capacity, self.key_table, self.hash_table
        )
        if self.hash_table[index] is None:
            self.length += 1

        self.key_table[index] = key
        self.hash_table[index] = key_hash
        self.value_table[index] = value

    def __len__(self) -> int:
        return self.length

    def clear(self) -> None:
        self.length = 0
        self.key_table: list = [None] * self.capacity
        self.hash_table: list = [None] * self.capacity
        self.value_table: list = [None] * self.capacity

    def __delitem__(self, key: Hashable) -> None:
        self.pop(key)

    def pop(self, key: Hashable) -> Any:
        key_hash = hash(key)
        index = self._find_index(
            key, key_hash, self.capacity, self.key_table, self.hash_table
        )
        if self.hash_table[index] is None:
            raise KeyError
        value = self.value_table[index]
        self.key_table[index] = None
        self.hash_table[index] = None
        self.value_table[index] = None
        return value

    def update(self, other_dict: Dictionary) -> None:
        for index, key_hash in enumerate(other_dict.hash_table):
            if key_hash is not None:
                self.__setitem__(
                    other_dict.key_table[index],
                    other_dict.value_table[index]
                )

    def __iter__(self) -> Iterator[Hashable]:
        return [key for key in self.key_table if key is not None].__iter__()
