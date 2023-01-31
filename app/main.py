from typing import Any, Hashable


class Node:
    def __init__(self, key: Hashable,
                 value: Any) -> None:
        try:
            self.my_hash = hash(key)
        except TypeError:
            print("It's a unhashable key!")
        else:
            self.key = key
            self.value = value
            self.next = None

    def __repr__(self) -> str:
        return f"Node(key: {self.key}, " \
               f"value: {self.value}, " \
               f"next: {self.next},\n)"


class Dictionary:
    def __init__(self) -> None:
        self.DEFAULT_CAPACITY = 8
        self.THRESHOLD = 2 / 3
        self.capacity = self.DEFAULT_CAPACITY
        self.data = [None] * self.DEFAULT_CAPACITY
        self.size = 0

    def get_index(self, key: Hashable) -> int:
        try:
            res = hash(key) % len(self.data)
        except TypeError:
            raise KeyError
        return res

    def __setitem__(self, key: Hashable,
                    value: Any) -> None:
        if self.size > len(self.data) * self.THRESHOLD:
            self.data = self.data + [None] * len(self.data)
        node = Node(key, value)
        index = self.get_index(key)
        for item in self.data:
            if item:
                if item.key == key:
                    item.value = value
                    return
                else:
                    current_node = item
                    while current_node and current_node.key != key:
                        current_node = current_node.next

                    if current_node:
                        current_node.value = value
                        return

        if self.data[index]:
            current_node = self.data[index]

            while current_node.next is not None:
                current_node = current_node.next
            current_node.next = node
            self.size += 1
        else:
            self.data[index] = node
            self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        for item in self.data:
            if item:
                if item.key == key:
                    return item.value
                else:
                    current_node = item
                    while current_node and current_node.key != key:
                        current_node = current_node.next
                    if current_node:
                        return current_node.value
        raise KeyError(key)

    def __len__(self) -> None:
        return self.size

    def clear(self) -> None:
        self.capacity = self.DEFAULT_CAPACITY
        self.data = [None] * self.capacity
        self.size = 0

    def __delitem__(self, key: Hashable) -> Any:
        if self.__getitem__(key):
            for item in self.data:
                if item:
                    if item.key == key:
                        item = item.next
                        return item
                    else:
                        item.next = None
                        current_node = item
                        while current_node and current_node.key != key:
                            current_node = current_node.next
                        if current_node:
                            return current_node
        self.size -= 1

    def get(self, key: Hashable) -> Any:
        for item in self.data:
            if item:
                if item.key == key:
                    return item.value
                else:
                    current_node = item
                    while current_node and current_node.key != key:
                        current_node = current_node.next
                    if current_node:
                        return current_node.value

    def pop(self, key: Hashable) -> Any:
        for item in self.data:
            if item:
                if item.key == key:
                    res = item
                    item = item.next
                    return res.value
                else:
                    item.next = None
                    current_node = item
                    while current_node and current_node.key != key:
                        current_node = current_node.next
                    if current_node:
                        return current_node.value
        self.size -= 1

    def update(self, key: Hashable, value: Any) -> Any:
        for item in self.data:
            if item:
                if item.key == key:
                    item.value = value
                    return
                else:
                    current_node = item
                    while current_node and current_node.key != key:
                        current_node = current_node.next

                    if current_node:
                        current_node.value = value
                        current_node.next = None
                        return

    def __iter__(self) -> None:
        return self
