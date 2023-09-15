from typing import Hashable, Any


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)
        self.next = None


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.buckets = [None] * self.capacity

    def __len__(self) -> int:
        return self.size

    def hash(self, key: Hashable) -> int:
        return abs(hash(key)) % self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self.hash(key)
        node = Node(key, value)
        if not self.buckets[index]:
            self.buckets[index] = node
            self.size += 1
        else:
            cur_node = self.buckets[index]
            while cur_node is not None:
                if cur_node.key == key:
                    cur_node.value = value
                    return
                if not cur_node.next:
                    break
                cur_node = cur_node.next
            cur_node.next = node
            self.size += 1
        if self.size / self.capacity > 2 / 3:
            self._resize()

    def __getitem__(self, key: Hashable) -> None:
        index = self.hash(key)
        cur_node = self.buckets[index]
        while cur_node:
            if cur_node.key == key and cur_node.hash == hash(key):
                return cur_node.value
            cur_node = cur_node.next
        raise KeyError("Key not found")

    def __delitem__(self, key: Hashable) -> None:
        index = self.hash(key)
        prev_node = None
        node = self.buckets[index]
        while node is not None and node.key != key:
            prev_node = node
            node = node.next
        if node is None:
            raise KeyError("Key not found")
        else:
            if prev_node is None:
                self.buckets[index] = node.next
            else:
                prev_node.next = node.next
            self.size -= 1

    def clear(self) -> None:
        self.buckets = [None] * self.capacity

    def _resize(self) -> None:
        old_capacity = self.capacity
        old_buckets = self.buckets

        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.size = 0

        for i in range(old_capacity):
            node = old_buckets[i]
            while node is not None:
                next_node = node.next
                if node.key is not None:
                    self.__setitem__(node.key, node.value)
                node = next_node
