from typing import Hashable, Any
import copy


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value
        self.next = None


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 8,
            load_factor: float = 2 / 3
    ) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:

        index = self._get_index(key)
        current = self.table[index]
        new_node = Node(key, value)
        if current is None:
            self.table[index] = new_node
        else:
            if current.key == key:
                current.value = value
                return
            index = self.index_plus(index)
            current = self.table[index]

            while current is not None:
                if current.key == key:
                    current.value = value
                    return
                index = self.index_plus(index)
                current = self.table[index]

            self.table[index] = new_node

        self.size += 1
        self._check_resize()

    def index_plus(self, index: int) -> int:
        return (index + 1) % self.capacity

    def __getitem__(self, key: Hashable) -> Any:
        index = self._get_index(key)
        current = self.table[index]
        while current is not None:
            if current.key == key:
                return current.value
            index = self.index_plus(index)
            current = self.table[index]
        raise KeyError(key)

    def _check_resize(self) -> None:
        if self.size / self.capacity >= self.load_factor:
            self._resize()

    def _resize(self) -> None:
        self.capacity *= 2
        copy_table = copy.deepcopy(self.table)
        self.table = [None] * self.capacity
        self.size = 0
        print(copy_table)
        for node in copy_table:
            if node is not None:
                self.__setitem__(node.key, node.value)
        del copy_table

    def _get_index(self, key: Hashable) -> int:
        hash_ = hash(key) % self.capacity
        return hash_

    def __len__(self) -> int:
        return self.size
