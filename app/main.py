from math import floor
from typing import Any


class Dictionary:
    DELETED = object()

    def __init__(self) -> None:
        self.buckets = [[None, None, None] for _ in range(8)]
        self.capacity = 8
        self.size = 0

    def __repr__(self) -> str:
        dict_buckets = [self.buckets[i] for i in range(self.capacity)]
        return f"DICT -> {dict_buckets}"

    def length(self) -> int:
        return self.size

    def save(self, key: Any, value: Any) -> None:
        key_hash = hash(key)
        position_in_dict = abs(key_hash) % self.capacity
        first_deleted_position = 0
        deleted_found = False
        rounds = 0
        while True:
            if self.buckets[position_in_dict][0] is None:
                if deleted_found:
                    position_in_dict = first_deleted_position
                self.buckets[position_in_dict][0] = key
                self.buckets[position_in_dict][1] = key_hash
                self.buckets[position_in_dict][2] = value
                self.size += 1
                break
            if (self.buckets[position_in_dict][0] is self.DELETED
                    and not deleted_found):
                first_deleted_position = position_in_dict
                deleted_found = True
            if self.buckets[position_in_dict][0] is not None:
                if self.buckets[position_in_dict][0] == key:
                    self.buckets[position_in_dict][0] = key
                    self.buckets[position_in_dict][1] = key_hash
                    self.buckets[position_in_dict][2] = value
                    break
            position_in_dict += 1
            if position_in_dict > self.capacity - 1:
                position_in_dict = 0
            rounds += 1
            if rounds == self.capacity:
                raise Exception("!!! DICTIONARY FULL !!!")

    def grow_dict(self) -> None:
        temp_buckets = []
        for bucket in self.buckets:
            if bucket[0] is not None and bucket[0] is not self.DELETED:
                temp_buckets += [bucket]
        self.capacity = self.capacity * 2
        self.clear()
        for bucket in temp_buckets:
            self.save(bucket[0], bucket[2])

    def clear(self) -> None:
        self.buckets = [[None, None, None] for _ in range(self.capacity)]
        self.size = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length() >= floor(self.capacity * 2 / 3):
            self.grow_dict()
        self.save(key, value)

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        position_in_dict = abs(key_hash) % self.capacity
        rounds = 0
        while True:
            if self.buckets[position_in_dict][0] is None:
                raise KeyError("!!! NO KEY OF THIS NAME !!!")
            if self.buckets[position_in_dict][0] == key:
                return self.buckets[position_in_dict][2]
            position_in_dict += 1
            if position_in_dict > self.capacity - 1:
                position_in_dict = 0
            rounds += 1
            if rounds == self.capacity:
                raise KeyError("!!! NO KEY OF THIS NAME !!!")

    def __delitem__(self, key: Any) -> None:
        key_hash = hash(key)
        position_in_dict = abs(key_hash) % self.capacity
        rounds = 0
        while True:
            if self.buckets[position_in_dict][0] is None:
                raise KeyError("!!! NO KEY OF THIS NAME !!!")
            if self.buckets[position_in_dict][0] == key:
                self.buckets[position_in_dict] = [self.DELETED, None, None]
                self.size -= 1
                return
            position_in_dict += 1
            if position_in_dict > self.capacity - 1:
                position_in_dict = 0
            rounds += 1
            if rounds == self.capacity:
                raise KeyError("!!! NO KEY OF THIS NAME !!!")

    def __len__(self) -> int:
        return self.length()
