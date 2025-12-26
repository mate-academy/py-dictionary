from typing import Hashable, Any


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self._capacity = capacity
        self._load_factor = 0.75
        self._size = 0
        self._table = [None] * capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_key, index = self._get_hash_and_index(key)
        node = key, hash_key, value
        i = self._find_node_index(index, key, hash_key)
        if i is None:
            self._append_node(index, node)
        else:
            self._replace_node(index, i, node)
        if self._size / self._capacity > self._load_factor:
            self._resize()

    def _get_hash_and_index(self, key: Hashable) -> Any:
        hash_key = hash(key)
        index = hash_key % self._capacity
        return hash_key, index

    def _find_node_index(self,
                         index: int,
                         key: Hashable,
                         hash_key: int) -> Any:
        if self._table[index] is None:
            return None
        else:
            for i in range(len(self._table[index])):
                if (self._table[index][i][0] == key
                        and self._table[index][i][1] == hash_key):
                    return i
            return None

    def _append_node(self, index: int, node: Any) -> None:
        if self._table[index] is None:
            self._table[index] = [node]
        else:
            self._table[index].append(node)
        self._size += 1

    def _replace_node(self, index: int, i: int, node: Any) -> None:
        self._table[index][i] = node

    def __getitem__(self, key: Hashable) -> None:
        hash_key = hash(key)
        index = hash_key % self._capacity
        if self._table[index] is None:
            raise KeyError(key)
        else:
            for node in self._table[index]:
                if node[1] == hash_key and node[0] == key:
                    return node[2]
            raise KeyError(key)

    def __len__(self) -> int:
        return self._size

    def _resize(self) -> None:
        old_table = self._table
        self._capacity *= 2
        self._table = [None] * self._capacity
        self._size = 0
        for cell in old_table:
            if cell is not None:
                for node in cell:
                    self.__setitem__(node[0], node[2])
