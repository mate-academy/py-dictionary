from typing import Any, Hashable, Optional


class Dictionary:
    def __init__(self) -> None:
        self.size = 0
        self.capacity = 8
        self.hash_table: list = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hsh = hash(key)
        idx = hsh % len(self.hash_table)
        node = self.hash_table[idx]
        if node is None:
            self.hash_table[idx] = Node(key, hsh, value)
            self.size += 1
        else:
            while node is not None:
                if hsh == node.hsh and node.key == key:
                    node.value = value
                    return
                node = node.next_iter
            new_node = Node(key, hsh, value)
            new_node.next_iter = self.hash_table[idx]
            self.hash_table[idx] = new_node
            self.size += 1

        if self.size > self.capacity * 0.75:
            self.__resize__()

    def __getitem__(self, key: Hashable) -> Any:
        hsh = hash(key)
        idx = hsh % len(self.hash_table)
        head = self.hash_table[idx]
        while head is not None:
            if hsh == head.hsh and head.key == key:
                return head.value
            head = head.next_iter
        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.size

    def __resize__(self) -> None:
        old_table = self.hash_table
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity
        for head in old_table:
            node = head
            while node:
                next_node = node.next_iter
                new_idx = node.hsh % new_capacity
                node.next_iter = new_table[new_idx]
                new_table[new_idx] = node
                node = next_node
        self.capacity = new_capacity
        self.hash_table = new_table


class Node:
    def __init__(self,
                 key: Hashable,
                 hsh: int,
                 value: Any,
                 next_iter: Optional = None
                 ) -> None:
        self.key = key
        self.hsh = hsh
        self.value = value
        self.next_iter = next_iter
