from typing import Hashable, Any


class Node:
    def __init__(self, key: Hashable, hash_val: int, value: Any) -> None:
        self.key = key
        self.hash_val = hash_val
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.lenght = 0
        self.hash_table = [None] * self.capacity
        self.load_factor = 2 / 3
        self.stop_line = self.capacity * self.load_factor

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_val = hash(key)
        index = hash_val % self.capacity
        if not self.hash_table[index]:
            self.hash_table[index] = [Node(key, hash_val, value)]
        else:
            for node in self.hash_table[index]:
                if node.hash_val == hash_val and node.key == key:
                    node.value = value
                    return
            self.hash_table[index].append(Node(key, hash_val, value))
        self.lenght += 1
        if self.lenght >= self.capacity * self.load_factor:
            self.resize()

    def __getitem__(self, key: Hashable) -> Any:
        hash_val = hash(key)
        index = hash_val % self.capacity
        if self.hash_table[index]:
            for node in self.hash_table[index]:
                if node.hash_val == hash_val and node.key == key:
                    return node.value
        raise KeyError(key)

    def __len__(self) -> int:
        return self.lenght

    def resize(self) -> None:
        new_capacity = self.capacity * 2
        new_hash_table = [None] * new_capacity
        for i in range(self.capacity):
            if self.hash_table[i]:
                for node in self.hash_table[i]:
                    new_index = node.hash_val % new_capacity
                    if new_hash_table[new_index] is None:
                        new_hash_table[new_index] = [node]
                    else:
                        new_hash_table[new_index].append(node)
        self.capacity = new_capacity
        self.hash_table = new_hash_table
