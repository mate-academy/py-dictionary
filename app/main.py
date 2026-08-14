from math import floor
from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.__size = 0
        self.__hash_table: list = [None] * 8
        self.__capacity = len(self.__hash_table)
        self.__threshold = floor(self.__capacity / 3 * 2)

    def __len__(self) -> int:
        return self.__size

    def __resize_hash_table(self) -> None:
        self.__capacity = self.__capacity * 2
        self.__threshold = floor(self.__capacity / 3 * 2)
        new_hash_table = [None] * self.__capacity

        for node in self.__hash_table:
            if node is None:
                continue

            hash_value = node["hash"]
            index = hash_value % self.__capacity

            if new_hash_table[index] is None:
                new_hash_table[index] = node
                continue

            for i in range(self.__capacity):
                available_index = (index + i) % self.__capacity

                if new_hash_table[available_index] is None:
                    new_hash_table[available_index] = node
                    break

        del self.__hash_table
        self.__hash_table = new_hash_table

    def __getitem__(self, key: Any) -> Any:
        hash_value = hash(key)
        index = hash_value % self.__capacity

        if self.__hash_table[index] is None:
            raise KeyError(f"Cannot find key {key}")

        if (
            self.__hash_table[index]["key"] == key
            and self.__hash_table[index]["hash"] == hash_value
        ):
            return self.__hash_table[index]["value"]

        for i in range(self.__capacity):
            current_index = (index + i) % self.__capacity

            if (
                self.__hash_table[current_index]["key"] == key
                and self.__hash_table[current_index]["hash"] == hash_value
            ):
                return self.__hash_table[current_index]["value"]

        raise KeyError(f"Cannot find key {key}")

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.__size == self.__threshold:
            self.__resize_hash_table()

        hash_value = hash(key)
        index = hash_value % self.__capacity

        if self.__hash_table[index] is None:
            self.__hash_table[index] = {
                "key": key,
                "hash": hash_value,
                "value": value,
            }
            self.__size += 1
            return

        if (
            key == self.__hash_table[index]["key"]
            and self.__hash_table[index]["hash"] == hash_value
        ):
            self.__hash_table[index]["value"] = value
            return

        for i in range(self.__capacity):
            available_index = (index + i) % self.__capacity

            if self.__hash_table[available_index] is None:
                self.__hash_table[available_index] = {
                    "key": key,
                    "hash": hash_value,
                    "value": value,
                }
                self.__size += 1
                return

            if (
                self.__hash_table[available_index]["key"] == key
                and self.__hash_table[available_index]["hash"] == hash_value
            ):
                self.__hash_table[available_index]["value"] = value
                return

        raise KeyError(f"Cannot set {value} to {key}")

    def __delitem__(self, key: Any) -> None:
        hash_value = hash(key)
        index = hash_value % self.__capacity
        node = self.__hash_table[index]

        if node:
            if node["key"] == key and node["hash"] == hash_value:
                self.__size -= 1
                del node
                self.__hash_table[index] = None
                return

        for i in range(self.__capacity):
            current_index = (index + i) % self.__capacity

            if self.__hash_table[current_index] is None:
                continue

            if (
                self.__hash_table[current_index]["key"] == key
                and self.__hash_table[current_index]["hash"] == hash_value
            ):
                self.__hash_table[current_index] = None
                return

        raise KeyError(f"Cannot delete key {key}")
