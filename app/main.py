from typing import Any


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(self.key)


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.hash_table = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        node = Node(key, value)

        place_in_table = node.hash % self.capacity

        while self.hash_table[place_in_table] is not None:
            if self.hash_table[place_in_table].key == key:
                self.hash_table[place_in_table].value = value
                return

            place_in_table += 1

            if place_in_table == self.capacity:
                place_in_table = 0

        self.hash_table[place_in_table] = node
        self.length += 1

        if self.length / self.capacity > 0.7:
            old_table = self.hash_table

            self.capacity *= 2
            self.hash_table = [None] * self.capacity

            for old_node in old_table:
                if old_node is not None:
                    new_place = old_node.hash % self.capacity

                    while self.hash_table[new_place] is not None:
                        new_place += 1

                        if new_place == self.capacity:
                            new_place = 0

                    self.hash_table[new_place] = old_node

    def __getitem__(self, key: Any) -> Any:
        node_hash = hash(key)
        place_in_table = node_hash % self.capacity

        while self.hash_table[place_in_table] is not None:
            if self.hash_table[place_in_table].key == key:
                return self.hash_table[place_in_table].value

            place_in_table += 1

            if place_in_table == self.capacity:
                place_in_table = 0

        raise KeyError("No key found")

    def __len__(self) -> int:
        return self.length
