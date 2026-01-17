from typing import Any


class Dictionary:
    INC_SIZE_TWICE = 2
    SIZE = 8

    def __init__(self) -> None:
        self.capacity = 0
        self.hash_table = [None] * Dictionary.SIZE

    def __setitem__(self, key: Any, value: Any) -> None:
        if isinstance(key, (list, dict, set)):
            raise KeyError("key must be hashable")

        # rewrite value, if we have the same key
        if self.check_rewrite_value(key, value):
            return

        # recount dict size, if too load
        if self.capacity > Dictionary.SIZE * 2 // 3:
            self.resize_dict()

        # check collision
        hash_key = hash(key)
        index = hash_key % Dictionary.SIZE
        index = self.check_collision_for_write(self.hash_table, index)
        self.hash_table[index] = Node(hash_key, key, value)
        self.capacity += 1

    def __getitem__(self, key_item: Any) -> Any:
        if isinstance(key_item, (list, dict, set)):
            raise KeyError("key must be hashable")
        return self.check_return_value(key_item)

    def __len__(self) -> int:
        return self.capacity

    @staticmethod
    def check_collision_for_write(table_to_check: list, index: int) -> int:
        while True:
            if table_to_check[index] is not None:
                index += 1
                if index >= (Dictionary.SIZE - 1):
                    index = 0
            else:
                break
        return index

    def resize_dict(self) -> None:
        Dictionary.SIZE *= Dictionary.INC_SIZE_TWICE
        new_hash_table = [None] * Dictionary.SIZE
        for item in self.hash_table:
            if item:
                index = hash(item.key) % Dictionary.SIZE
                index = self.check_collision_for_write(new_hash_table, index)
                new_hash_table[index] = item
        self.hash_table = new_hash_table

    def check_rewrite_value(self, key: Any, value: Any) -> bool:
        hash_key = hash(key)
        index = hash_key % Dictionary.SIZE
        while self.hash_table[index]:
            item = self.hash_table[index]
            if item.hash == hash_key and item.key == key:
                item.value = value
                return True
            index += 1
            if index >= Dictionary.SIZE - 1:
                index = 0
        return False

    def check_return_value(self, key: Any) -> bool | None:
        hash_key = hash(key)
        index = hash_key % Dictionary.SIZE
        while self.hash_table[index]:
            item = self.hash_table[index]
            if item.hash == hash_key and item.key == key:
                return item.value
            index += 1
            if index >= Dictionary.SIZE - 1:
                index = 0
        raise KeyError("key not in dict")


class Node:
    def __init__(self, hash_: int, key: Any, value: Any) -> None:
        self.hash = hash_
        self.key = key
        self.value = value
