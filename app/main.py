from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.threshold = 0.67 * self.capacity
        self.bucket = [[]] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        empty_slot = hash(key) % self.capacity
        while True:
            if not self.bucket[empty_slot]:
                self.bucket[empty_slot] = [key, hash(key), value]
                self.length += 1
                break
            if self.bucket[empty_slot][0] == key and (
                    self.bucket[empty_slot][1] == hash(key)):
                self.bucket[empty_slot][2] = value
                break
            empty_slot = (empty_slot + 1) % self.capacity
        if self.length > self.threshold:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        empty_slot = hash(key) % self.capacity
        while self.bucket[empty_slot]:
            if key == self.bucket[empty_slot][0] and (
                    self.bucket[empty_slot][1] == hash(key)):
                return self.bucket[empty_slot][2]
            empty_slot = (empty_slot + 1) % self.capacity
        raise KeyError(key)

    def __len__(self) -> int:
        return self.length

    def _resize(self) -> None:
        bucket_old = self.bucket
        self.threshold *= 2
        self.capacity *= 2
        self.length = 0
        self.bucket = [[]] * self.capacity
        for slot in bucket_old:
            if slot:
                self.__setitem__(slot[0], slot[2])
