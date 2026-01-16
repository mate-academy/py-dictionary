from dataclasses import dataclass, field
from typing import Hashable


@dataclass
class Dictionary:
    capacity: int = 8
    load_factor: float = 0.75
    size: int = 0
    table: list = field(init=False)

    def __post_init__(self) -> None:
        self.table = self.capacity * [None]

    def resize_table(self) -> list:
        self.size = 0
        self.capacity *= 2
        new_table = self.capacity * [None]
        for node in self.table:
            if not node:
                continue
            hash_value = hash(node[0])
            num_of_hash_table = hash_value % self.capacity
            while True:
                if not new_table[num_of_hash_table]:
                    new_table[num_of_hash_table] = [
                        node[0],
                        node[1]
                    ]
                    self.size += 1
                    break
                num_of_hash_table += 1
                if num_of_hash_table == self.capacity:
                    num_of_hash_table = 0
        return new_table.copy()

    def __setitem__(self, key: Hashable, value: object) -> None:
        if (self.size + 1) > self.capacity * self.load_factor:
            self.table = self.resize_table()

        hash_value = hash(key)
        num_of_hash_table = hash_value % self.capacity
        while True:
            if not self.table[num_of_hash_table]:
                self.table[num_of_hash_table] = [key, value]
                self.size += 1
                break
            elif self.table[num_of_hash_table][0] == key:
                self.table[num_of_hash_table] = [key, value]
                break
            num_of_hash_table = (num_of_hash_table + 1) % self.capacity

    def __getitem__(self, item: Hashable) -> object:
        hash_value = hash(item)
        num_of_hash_table = hash_value % self.capacity
        while True:
            if not self.table[num_of_hash_table]:
                raise KeyError
            if self.table[num_of_hash_table][0] != item:
                num_of_hash_table = (num_of_hash_table + 1) % self.capacity
            else:
                return self.table[num_of_hash_table][1]

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.capacity = 8
        self.load_factor = 0.75
        self.size = 0
        self.table = self.capacity * [None]

    def __delitem__(self, key: Hashable) -> None:
        hash_value = hash(key)
        num_of_hash_table = hash_value % self.capacity
        while True:
            if not self.table[num_of_hash_table]:
                print(f"Key '{key}' not found")
                return
            if self.table[num_of_hash_table][0] == key:
                self.table[num_of_hash_table] = None
                self.size -= 1
                return
            num_of_hash_table = (num_of_hash_table + 1) % self.capacity

    def get(self, key: Hashable, *arg: object) -> object | None:
        hash_value = hash(key)
        num_of_hash_table = hash_value % self.capacity
        while True:
            if not self.table[num_of_hash_table]:
                if arg:
                    return arg
                return None
            if self.table[num_of_hash_table][0] != key:
                num_of_hash_table = (num_of_hash_table + 1) % self.capacity
            else:
                return self.table[num_of_hash_table][1]

    def pop(self, key: Hashable, *arg: object) -> object:
        hash_value = hash(key)
        num_of_hash_table = hash_value % self.capacity
        while True:
            if not self.table[num_of_hash_table]:
                if arg:
                    return arg
                raise Exception("Dict does not have such a key")

            if self.table[num_of_hash_table][0] == key:
                value = self.table[num_of_hash_table][1]
                self.table[num_of_hash_table] = None
                self.size -= 1
                return value
            num_of_hash_table = (num_of_hash_table + 1) % self.capacity

    def items(self) -> list:
        list_items = []
        for node in self.table:
            if node:
                list_items.append((node[0], node[1]))
        return list_items

    def update(self, other: "Dictionary") -> None:
        for node in other.items():
            self.__setitem__(self, *node)

    def __iter__(self) -> iter:
        for node in self.table:
            if node:
                yield node[0]
