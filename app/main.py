from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.hashmap: list = [[] for _ in range(self.capacity)]
        self.length = 0
        self.LOAD_FACTOR = 0.75

    def hash_key_index(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def resize(self) -> None:
        self.capacity *= 2
        new_hashmap = [[] for _ in range(self.capacity)]

        for bucket in self.hashmap:
            for key, value, hash_key in bucket:
                new_hashmap[self.hash_key_index(key)].append(
                    (key, value, hash_key)
                )

        self.hashmap = new_hashmap

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_key = hash(key)
        bucket = self.hashmap[self.hash_key_index(key)]

        for index, (stored_key, stored_value, stored_hash) \
                in enumerate(bucket):
            if stored_hash == hash_key and stored_key == key:
                bucket[index] = (key, value, hash_key)
                self.length -= 1
                break

        bucket.append((key, value, hash_key))
        self.length += 1

        if self.length / float(self.capacity) >= self.LOAD_FACTOR:
            self.resize()

    def __getitem__(self, key: Hashable) -> Any:
        bucket = self.hashmap[self.hash_key_index(key)]
        for stored_key, stored_value, _ in bucket:
            if stored_key == key:
                return stored_value
        raise KeyError("Key doesn't exist.")

    def __len__(self) -> int:
        return self.length
