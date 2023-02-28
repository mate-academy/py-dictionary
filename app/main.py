from typing import Hashable, Any, Iterable


class Dictionary:
    def __init__(self) -> None:
        self._capacity = 8
        self._load_factor = 2 / 3
        self._current_load = 0
        self._hash_table = [None] * self._capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        node = (key, hash(key), value)
        if self._check_existing_key(node):
            return

        self._current_load += 1

        self._check_for_resizing()

        index = hash(key) % self._capacity
        index = self._find_empty_node(self._hash_table, index)
        self._hash_table[index] = node

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self._capacity
        if (
                not self._hash_table[index]
                and self._hash_table[(index + 1) % self._capacity]
        ):
            index += 1
            index %= self._capacity
        while self._hash_table[index]:
            if self._hash_table[index][0] == key:
                return self._hash_table[index][2]
            index += 1
            index %= self._capacity
        raise KeyError

    def __len__(self) -> int:
        return self._current_load

    def __delitem__(self, key: Hashable) -> None:
        index = hash(key) % self._capacity
        while self._hash_table[index]:
            if self._hash_table[index][0] == key:
                self._hash_table[index] = None
                return
            index += 1
            index %= self._capacity
        raise KeyError

    def __iter__(self) -> object:
        return iter(node for node in self._hash_table if node)

    def _check_existing_key(self, node: tuple) -> bool:
        index = node[1] % self._capacity
        while self._hash_table[index]:
            if self._hash_table[index][0] == node[0]:
                self._hash_table[index] = node
                return True
            index += 1
            index %= self._capacity
        return False

    def _check_for_resizing(self) -> None:
        if self._current_load >= self._capacity * self._load_factor:
            self._capacity *= 2
            new_hash_table = [None] * self._capacity
            for exist_node in [node for node in self._hash_table if node]:
                index = exist_node[1] % self._capacity
                index = self._find_empty_node(new_hash_table, index)
                new_hash_table[index] = exist_node
            self._hash_table = new_hash_table

    def _find_empty_node(self, hash_table: list, index: int) -> int:
        while hash_table[index]:
            index += 1
            index %= self._capacity
        return index

    def clear(self) -> None:
        self._hash_table = None

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = None) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default:
                return default
            raise KeyError

    def update(self, new_items: Iterable) -> None:
        for item in new_items:
            self[item[0]] = item[-1]
