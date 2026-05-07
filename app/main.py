from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.load_factor = 2 / 3
        self.capacity = 8
        self.hash_list: list = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        index = hash(key) % self.capacity
        key_hash = hash(key)
        while self.hash_list[index] is not None:
            if (self.hash_list[index][0] == key_hash
                    and self.hash_list[index][1] == key):
                self.hash_list[index] = [key_hash, key, value]
                return

            index = (index + 1) % self.capacity

        self.hash_list[index] = [key_hash, key, value]
        self.length += 1

        if self.length > self.load_factor * self.capacity:
            old_hash_list = self.hash_list
            self.capacity *= 2
            self.hash_list: list = [None] * self.capacity
            self.length = 0

            for obj in old_hash_list:
                if obj is not None:
                    self.__setitem__(obj[1], obj[2])

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity
        while self.hash_list[index] is not None:
            key_hash, old_key, value = self.hash_list[index]
            if key_hash == hash(key) and old_key == key:
                return value

            index = (index + 1) % self.capacity

        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.length
