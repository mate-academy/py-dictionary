from typing import Any, List, Optional

DEFAULT_CAPACITY = 8
LOAD_FACTOR = 2 / 3


class DictionaryNode:
    __slots__ = ("key", "hash", "value")

    def __init__(self, key: Any, h: int, value: Any) -> None:
        self.key = key
        self.hash = h
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = DEFAULT_CAPACITY
        self.hash_table: List[Optional[DictionaryNode]] = ([None]
                                                           * self.capacity)
        self.filled_count = 0
        self.threshold = int(self.capacity * LOAD_FACTOR)

    def __len__(self) -> int:
        return self.length

    def _get_hash(self, key: Any) -> int:
        try:
            return hash(key)
        except TypeError:
            raise TypeError(f"Key of type '{type(key).__name__}' "
                            f"is not hashable.")

    def _get_index(self, h: int) -> int:
        return h & (self.capacity - 1)

    def _place_node_at_new_index(self, node: DictionaryNode) -> None:
        index = self._get_index(node.hash)

        while self.hash_table[index] is not None:
            index = (index + 1) & (self.capacity - 1)

        self.hash_table[index] = node

    def _add_node_internal(self, node: DictionaryNode) -> None:
        self._place_node_at_new_index(node)
        self.length += 1
        self.filled_count += 1

    def _resize(self) -> None:
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.filled_count = 0
        self.threshold = int(self.capacity * LOAD_FACTOR)

        for node in old_table:
            if node is not None:
                self._place_node_at_new_index(node)
                self.filled_count += 1

    def __setitem__(self, key: Any, value: Any) -> None:
        h = self._get_hash(key)
        index = self._get_index(h)

        start_index = index
        while self.hash_table[index] is not None:
            node = self.hash_table[index]

            if node.hash == h and node.key == key:
                node.value = value
                return

            index = (index + 1) & (self.capacity - 1)

            if index == start_index:
                break

        new_node = DictionaryNode(key, h, value)
        self._add_node_internal(new_node)

        if self.filled_count >= self.threshold:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        h = self._get_hash(key)
        index = self._get_index(h)

        start_index = index
        while self.hash_table[index] is not None:
            node = self.hash_table[index]

            if node.hash == h and node.key == key:
                return node.value

            index = (index + 1) & (self.capacity - 1)

            if index == start_index:
                break

        raise KeyError(f"Key '{key}' not found in the dictionary.")

    def clear(self) -> None:
        self.length = 0
        self.capacity = DEFAULT_CAPACITY
        self.hash_table = [None] * self.capacity
        self.filled_count = 0
        self.threshold = int(self.capacity * LOAD_FACTOR)

    def __delitem__(self, key: Any) -> None:
        h = self._get_hash(key)
        index = self._get_index(h)

        start_index = index
        while self.hash_table[index] is not None:
            node = self.hash_table[index]

            if node.hash == h and node.key == key:
                self.hash_table[index] = None
                self.length -= 1
                self.filled_count -= 1
                self._rehash_from_index(index)
                return

            index = (index + 1) & (self.capacity - 1)

            if index == start_index:
                break

        raise KeyError(f"Key '{key}' not found "
                       f"in the dictionary for deletion.")

    def _rehash_from_index(self, start_index: int) -> None:
        index = (start_index + 1) & (self.capacity - 1)

        while self.hash_table[index] is not None:
            node_to_move = self.hash_table[index]
            self.hash_table[index] = None
            self._place_node_at_new_index(node_to_move)
            index = (index + 1) & (self.capacity - 1)
