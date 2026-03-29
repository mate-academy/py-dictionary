from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * 8

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Any, value: Any) -> Any:
        hashed = hash(key)
        index = hashed % len(self.hash_table)
        list_of_node = []
        found_key = False

        if self.hash_table[index] is None:
            list_of_node.append(Node(key, hashed, value))
            self.hash_table[index] = list_of_node
            self.length += 1

        else:
            for stored_node in self.hash_table[index]:
                if stored_node.hashed == hashed:
                    if stored_node.key == key:
                        stored_node.value = value
                        found_key = True
                        break
            if found_key is False:
                self.hash_table[index].append(Node(key, hashed, value))
                self.length += 1

    def __getitem__(self, key: Any) -> Any:
        hashed = hash(key)
        index = hashed % len(self.hash_table)

        if self.hash_table[index] is None:
            raise KeyError

        else:
            for stored_node in self.hash_table[index]:
                if stored_node.hashed == hashed:
                    if stored_node.key == key:
                        return stored_node.value
            raise KeyError


class Node:
    def __init__(self, key: Any, hashed: Any, value: Any) -> None:
        self.key = key
        self.hashed = hashed
        self.value = value
