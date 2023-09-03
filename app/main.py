from app.dict_settings import DictSettings
from app.dict_settings import Node
from typing import Any, Hashable


class Dictionary(DictSettings):
    def __init__(self) -> None:
        self._capacity = DictSettings.capacity
        self._load_factor = DictSettings.load_factor
        self._length = 0
        self._hash_table: list = [None] * self._capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        item_index = self._get_index(key)
        if self._hash_table[item_index]:
            self._hash_table[item_index].value = value
        else:
            self._hash_table[item_index] = Node(
                key=key,
                value=value,
                hash_value=hash(key)
            )
            self._length += 1

        if self._length >= self._capacity * self._load_factor:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        item_index = self._get_index(key)
        if self._hash_table[item_index]:
            return self._hash_table[item_index].value
        raise KeyError

    def __delitem__(self, key: Hashable) -> None:
        item_index = self._get_index(key)
        self._hash_table[item_index] = None
        self._length -= 1

    def __len__(self) -> int:
        return self._length

    def _get_index(self, key: Hashable) -> int:
        item_index = hash(key) % self.capacity
        while not (
                self._hash_table[item_index] is None
                or (
                    self._hash_table[item_index].key == key
                    and self._hash_table[item_index].hash_value == hash(key)
                )
        ):
            item_index = (item_index + 1) % self._capacity
        return item_index

    def _resize(self) -> None:
        old_hash_table = [node for node in self._hash_table if node]
        self._capacity *= 2
        self.clear()
        for node in old_hash_table:
            self[node.key] = node.value

    def clear(self) -> None:
        self._length = 0
        self._hash_table = [None] * self._capacity
