from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.table = [[] for _ in range(self.capacity)]
        self.length = 0

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Any, value: Any) -> None:
        key_hash = hash(key)
        slot = key_hash % self.capacity
        counter = 0

        while counter < self.capacity:
            index = (slot + counter) % self.capacity
            node = self.table[index]

            if node == []:
                break

            if node[0][0] == key:
                node[0] = (key, key_hash, value)
                return

            counter += 1

        if self.length >= round(self.capacity * 0.66):
            old_table = self.table
            self.capacity *= 2
            self.table = [[] for _ in range(self.capacity)]

            for node in old_table:
                if node == []:
                    continue

                node_hash = node[0][1]
                slot = node_hash % self.capacity
                counter = 0

                while self.table[
                    (slot + counter) % self.capacity
                ] != []:
                    counter += 1

                self.table[
                    (slot + counter) % self.capacity
                ].append(node[0])

        slot = key_hash % self.capacity
        counter = 0

        while self.table[(slot + counter) % self.capacity] != []:
            counter += 1

        self.table[
            (slot + counter) % self.capacity
        ].append((key, key_hash, value))

        self.length += 1

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        slot = key_hash % self.capacity

        for counter in range(self.capacity):
            index = (slot + counter) % self.capacity
            node = self.table[index]

            if node == []:
                continue

            if node[0][0] == key:
                return node[0][2]

        raise KeyError(f"Key '{key}' not found")
