from typing import Any, Hashable


class Node:
    def __init__(self, key: Hashable, value: Any, hash_number: int) -> None:
        self.key = key
        self.value = value
        self.hash_number = hash_number


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.hash_table = [None] * self.capacity
        self.threshold = 2 / 3

    def resize_and_rehash_if_necessary(self) -> None:
        if self.__len__() + 1 >= self.capacity * self.threshold:
            self.capacity *= 2
            old_hash_table = self.hash_table
            self.hash_table = [None] * self.capacity

            for node in old_hash_table:
                if node is not None:
                    self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self.resize_and_rehash_if_necessary()

        hash_number = hash(key) % self.capacity
        node_object = Node(key, value, hash_number)

        index = node_object.hash_number

        if self.hash_table[index] is None:
            self.hash_table[index] = node_object

        elif self.hash_table[index].key == key:
            existing_node = self.hash_table[index]
            existing_node.value = value

        else:
            while True:
                index = (index + 1) % self.capacity
                if self.hash_table[index] is None:
                    self.hash_table[index] = node_object
                    break
                elif self.hash_table[index].key == key:
                    existing_node = self.hash_table[index]
                    existing_node.value = value
                    break

    def __getitem__(self, item: Any) -> Any:
        index = hash(item) % self.capacity
        for _ in range(self.capacity):
            element = self.hash_table[index]
            if element:
                if element.key == item:
                    return element.value
            index = (index + 1) % self.capacity
        raise KeyError

    def __len__(self) -> int:
        num_of_elements = 0
        for element in self.hash_table:
            if element:
                num_of_elements += 1
        return num_of_elements
