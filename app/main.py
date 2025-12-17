from typing import Any, Hashable, List, Optional


class Node:
    def __init__(self, key: Hashable, hash_key: int, value: Any) -> None:
        self.key = key
        self.hash_key = hash_key
        self.value = value


class Sentinel:
    pass


TOMBSTONE = Sentinel()


class Dictionary:
    def __init__(self) -> None:
        self.hash_table: List[Optional[Node]] = [None] * 8
        self.current_size = 0
        self.capacity = 8

    def _probe(self, key: Hashable, for_insert: bool = False) -> int:
        index = hash(key) % self.capacity
        start_index = index
        first_tombstone_index = -1

        while True:
            current_slot = self.hash_table[index]

            if current_slot is None:
                if for_insert and first_tombstone_index != -1:
                    return first_tombstone_index
                return index if for_insert else -1

            if current_slot is TOMBSTONE:
                if for_insert and first_tombstone_index == -1:
                    first_tombstone_index = index

            elif (current_slot.key == key and current_slot.hash_key
                  == hash(key)):
                return index

            index = (index + 1) % self.capacity

            if index == start_index:
                if for_insert and first_tombstone_index != -1:
                    return first_tombstone_index
                return index if for_insert else -1

    def __resize_hash_table(self) -> None:
        old_nodes = [node for node in self.hash_table
                     if node is not None and node is not TOMBSTONE]
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.current_size = 0

        for node in old_nodes:
            self[node.key] = node.value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.current_size + 1 > int(self.capacity * 0.66):
            self.__resize_hash_table()

        index = self._probe(key, for_insert=True)
        current = self.hash_table[index]

        if current is None:
            self.hash_table[index] = Node(key, hash(key), value)
            self.current_size += 1
        else:
            self.hash_table[index].value = value

    def __getitem__(self, key: Hashable) -> Any:
        index = self._probe(key)
        if index == -1 or self.hash_table[index] is None:
            raise KeyError(key)
        return self.hash_table[index].value

    def __len__(self) -> int:
        return self.current_size

    def clear(self) -> None:
        self.hash_table = [None] * self.capacity
        self.current_size = 0

    def __delitem__(self, key: Hashable) -> None:
        index = self._probe(key)
        if index == -1 or self.hash_table[index] is None:
            raise KeyError(key)

        self.hash_table[index] = TOMBSTONE
        self.current_size -= 1

    def get(self, key: Hashable, default_value: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default_value

    def pop(self, key: Hashable) -> Any:
        value = self[key]
        del self[key]
        return value

    def update(self, other: List[Node]) -> None:
        for node in other:
            self[node.key] = node.value

    def __iter__(self) -> object:
        self._iter_index = 0
        return self

    def __next__(self) -> Hashable:
        while self._iter_index < self.capacity:
            node = self.hash_table[self._iter_index]
            self._iter_index += 1
            if node is not None:
                return node.key
        raise StopIteration
