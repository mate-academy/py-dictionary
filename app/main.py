import copy
import pprint
from collections.abc import Hashable
from typing import Union, Any, Iterator


class Dictionary:
    def __init__(self) -> None:
        self.hash_table = [[] for _ in range(8)]
        self.collisions = []
        self.old_hash_table = None
        self.capacity = 8

    def resize(self) -> None:
        if not len(self) / self.capacity > 2 / 3:
            return

        """Resize"""
        self.capacity *= 2
        self.old_hash_table = copy.deepcopy(self.hash_table)
        self.hash_table = [[] for bucket in range(self.capacity)]
        self.collisions.clear()

        for bucket in self.old_hash_table:
            if len(bucket):
                self[bucket[0]] = bucket[1]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if not isinstance(key, Hashable):
            raise TypeError(f"unhashable type: '{type(key).__name__}'")

        index = hash(key) % self.capacity
        item = [key, value, hash(key)]

        """Empty bucket"""
        if not len(self.hash_table[index]):
            self.hash_table[index] = item
            self.resize()
            return

        """Reassign value"""
        if self.hash_table[index][0] == key:
            if self.hash_table[index][2] == hash(key):
                self.hash_table[index][1] = value
                return

        """Check old collisions"""
        for collision in self.collisions:
            if collision[0] == key:
                if hash(collision[0]) == hash(key):
                    collision_item_index = collision[1]
                    self.hash_table[collision_item_index][1] = value
                    return

        """New collision"""
        collision_item_index = self.hash_table.index([])
        self.hash_table[collision_item_index] = item
        self.collisions.append([key, collision_item_index])
        self.resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity

        if len(self.hash_table[index]):
            if self.hash_table[index][0] == key:
                return self.hash_table[index][1]

            for collision in self.collisions:
                if collision[0] == key:
                    index = collision[1]
                    return self.hash_table[index][1]

        raise KeyError(key)

    def __len__(self) -> int:
        return sum(1 for bucket in self.hash_table if len(bucket))

    def clear(self) -> None:
        self.hash_table = [[] for bucket in range(self.capacity)]

    def __delitem__(self, key: Hashable) -> None:
        item = self.hash_table[hash(key) % self.capacity]
        if item[0] == key:
            item.clear()
            return

        for collision in self.collisions:
            if collision[0] == key:
                if hash(collision[0]) == hash(key):
                    self.hash_table[collision[1]].clear()
                    return
        raise KeyError(key)

    def get(self, key: Hashable, default: Any = None) -> Any:
        self.__getitem__(key)

    def pop(self, key: Hashable, default: Any = None) -> Union[None, Any]:
        try:
            value = self.__getitem__(key)
            self.__delitem__(key)
            return value
        except KeyError:
            if default is not None:
                return default
            raise

    def update(self, other_dict: "Dictionary") -> None:
        for bucket in other_dict.hash_table:
            if len(bucket):
                self[bucket[0]] = bucket[1]

    def __iter__(self) -> Iterator:
        return iter(bucket[0] for bucket in self.hash_table if len(bucket))

    def __repr__(self) -> str:
        return ("CUSTOM_HASH_TABLE: [KEY, VALUE, HASH(KEY)]\n"
                + ("*" * 42) + "\n" + pprint.pformat(
                    object=self.hash_table,
                    indent=0)[1:-1]
                + "\n" + "CAPACITY: " + str(self.capacity) + "\n"
                + "LEN: " + str(self.__len__())) + "\n" + ("*" * 42)

    def __str__(self) -> str:
        return "{" + ", ".join([str(bucket[0]) + " : " + str(bucket[1])
                                for bucket in self.hash_table
                                if len(bucket)]) + "}"
