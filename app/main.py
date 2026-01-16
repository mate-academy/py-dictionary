class Node:
    def __init__(self, key: any, hash_key: int, value: any) -> None:
        self.key = key
        self.hash = hash_key
        self.value = value
        self.next = None


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.storage = [None] * 8
        self.load_factor = 2 / 3
        self.capacity = 8

    def _find_hash(self, key: any) -> int:
        return hash(key) % self.capacity

    def __len__(self) -> int:
        return self.length

    def __getitem__(self, item: any) -> any:
        index = self._find_hash(item)
        current = self.storage[index]
        while current:
            if current.key == item and current.hash == hash(item):
                return current.value
            current = current.next

        raise KeyError(item)

    def __setitem__(self, key: any, value: any) -> None:
        if self.length >= self.capacity * self.load_factor:
            self._resize()

        index = self._find_hash(key)
        new_node = Node(key, hash(key), value)

        if self.storage[index] is None:
            self.storage[index] = new_node
        else:
            current = self.storage[index]
            while current:
                if current.key == key and current.hash == hash(key):
                    current.value = value
                    return
                if current.next is None:
                    break
                current = current.next

            current.next = new_node
        self.length += 1

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity

        for bucket in self.storage:
            current = bucket
            while current:
                new_index = current.hash % new_capacity
                new_node = Node(current.key, current.hash, current.value)
                new_node.next = new_table[new_index]
                new_table[new_index] = new_node
                current = current.next

        self.storage = new_table
        self.capacity = new_capacity

    def __delitem__(self, key: any) -> None:
        index = self._find_hash(key)
        current = self.storage[index]
        prev = None

        while current:
            if current.key == key and current.hash == hash(key):
                if prev:
                    prev.next = current.next
                else:
                    self.storage[index] = current.next
                self.length -= 1
                return
            prev = current
            current = current.next

        raise KeyError(key)

    def clear(self) -> None:
        self.storage = [None] * 8
        self.capacity = 8
        self.length = 0

    def get(self, key: any) -> None:
        return self.__getitem__(key)

    def pop(self, key: any, default: any = None) -> None:

        try:
            value = self.__getitem__(key)
            self.__delitem__(key)
            return value
        except KeyError:
            return default

    def update(self, other_dict: dict) -> None:
        for key, value in other_dict.items():
            self.__setitem__(key, value)

    def __iter__(self) -> None:
        for item in self.storage:
            current = item
            while current:
                yield f"key = {current.key}, value = {current.value}"

                current = current.next
