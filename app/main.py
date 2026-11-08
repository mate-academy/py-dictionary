from typing import Any


class Node:
    def __init__(self, key: Any, value: Any, my_hash: int) -> None:
        self.key = key
        self.value = value
        self.hash = my_hash


class Dictionary:
    def __init__(self) -> None:
        self.hash_table = [None] * 8
        self.capacity = 8
        self.count = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.count >= (self.capacity * 2) // 3:
            self.capacity *= 2
            old_table = self.hash_table
            self.hash_table = [None] * self.capacity
            self.count = 0
            for element in old_table:
                if element:
                    self[element.key] = element.value

        self.h = hash(key)
        i = self.h % self.capacity
        item = Node(key, value, self.h)

        while True:
            if self.hash_table[i] is None:
                self.hash_table[i] = item
                self.count += 1
                break
            elif (
                self.hash_table[i] is not None
                and self.hash_table[i].key == item.key
            ):
                self.hash_table[i].value = value
                break
            else:
                i = (i + 1) % self.capacity

    def __getitem__(self, key: Any) -> Any:
        h = hash(key)
        i = h % self.capacity

        while True:
            if self.hash_table[i] is None:
                raise KeyError("KeyError")
            elif self.hash_table[i].key != key:
                i = (i + 1) % self.capacity
                continue
            else:
                return self.hash_table[i].value

    def __len__(self) -> int:
        return self.count
