import random
from typing import Optional


class Node:
    def __init__(self, key: str, value: str) -> None:
        self.key = key
        self.value = value
        self.hash_value = hash(key)


class Dictionary:
    def __init__(self) -> None:
        self.dictionary: list[Optional[Node]] = [None] * 8
        self.amount_of_node: int = 0

    def __setitem__(self, key: str, value: str) -> None:
        self.node = Node(key, value)
        if self.update_node():
            return
        if self.amount_of_node >= len(self.dictionary) * 2 / 3:
            self.change_size()
        self.add_node()

    def __getitem__(self, key: str) -> str:
        index = hash(key) % len(self.dictionary)
        node = self.dictionary[index]
        if node is not None and node.key == key:
            return node.value
        for node in self.dictionary:
            if node is not None and node.key == key:
                return node.value
        raise KeyError(key)

    def __len__(self) -> int:
        return self.amount_of_node

    def add_node(self) -> None:
        index = self.node.hash_value % len(self.dictionary)
        if self.dictionary[index] is None:
            self.dictionary[index] = self.node
        else:
            while True:
                random_index = random.randint(0, len(self.dictionary) - 1)
                if self.dictionary[random_index] is None:
                    self.dictionary[random_index] = self.node
                    break
        self.amount_of_node += 1

    def update_node(self) -> bool:
        index = self.node.hash_value % len(self.dictionary)
        if (
            self.dictionary[index] is not None
            and self.dictionary[index].key == self.node.key
        ):
            self.dictionary[index] = self.node
            return True
        for i, node in enumerate(self.dictionary):
            if (
                node is not None
                and node.hash_value == self.node.hash_value
                and node.key == self.node.key
            ):
                self.dictionary[i] = self.node
                return True
        return False

    def change_size(self) -> None:
        new_dictionary: list[Optional[Node]] = \
            [None] * (len(self.dictionary) * 2)
        for node in self.dictionary:
            if node is not None:
                index = node.hash_value % len(new_dictionary)
                if new_dictionary[index] is None:
                    new_dictionary[index] = node
                else:
                    while True:
                        random_index = random.randint(0, len(new_dictionary)
                                                      - 1)
                        if new_dictionary[random_index] is None:
                            new_dictionary[random_index] = node
                            break
        self.dictionary = new_dictionary
