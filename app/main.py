from typing import Any, Hashable


BASE_CAPACITY = 8


class Entry:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)
        self.is_deleted = False


class Dictionary:

    def __init__(self) -> None:
        self.__capacity = BASE_CAPACITY
        self.__hash_table = [None] * self.__capacity
        self.__count = 0

    def __setitem__(self, key: Hashable, value: Any) -> None:
        entry = Entry(key, value)
        index = self.calculate_index(key)
        while (self.__hash_table[index]
               and not self.__hash_table[index].is_deleted):
            if self.__hash_table[index].key == key:
                self.__hash_table[index].value = value
                return
            index = (index + 1) % self.__capacity
        self.__hash_table[index] = entry
        self.__count += 1
        if self.__count >= int(self.__capacity * 2 / 3):
            self.resize_and_rehash()

    def __getitem__(self, key: Hashable) -> Any:
        index = self.calculate_index(key)
        current_entry = self.__hash_table[index]
        while current_entry and not current_entry.is_deleted:
            if current_entry.key == key:
                return current_entry.value
            index = (index + 1) % self.__capacity
            current_entry = self.__hash_table[index]
        raise KeyError(f"Key {key} is not in dict")

    def __len__(self) -> int:
        return self.__count

    def clear(self) -> None:
        self.__hash_table = [None] * self.__capacity

    def __delitem__(self, key: Hashable) -> None:
        index = self.calculate_index(key)
        while self.__hash_table[index] and self.__hash_table[index].key != key:
            index = (index + 1) % self.__capacity
        self.__hash_table[index].is_deleted = True
        self.__count -= 1

    def pop(self, key: Hashable, default: Any = None) -> Any:
        index = self.calculate_index(key)
        current = self.__hash_table[index]
        while current:
            if current.key == key and not current.is_deleted:
                value = current.value
                self.__delitem__(key)
                return value
            index = (index + 1) % self.__capacity
            current = self.__hash_table[index]
        return default

    def update(self, *args: tuple[Hashable, Any]) -> None:
        for key, value in args:
            self[key] = value

    def resize_and_rehash(self) -> None:
        self.__capacity *= 2
        old_hash_table = self.__hash_table
        self.__hash_table = [None] * self.__capacity
        for entry in old_hash_table:
            if entry and not entry.is_deleted:
                index = self.calculate_index(entry.key)
                while self.__hash_table[index]:
                    index = (index + 1) % self.__capacity
                self.__hash_table[index] = entry

    def calculate_index(self, key: Hashable) -> int:
        index = hash(key) % self.__capacity
        while self.__hash_table[index] and self.__hash_table[index].key != key:
            index = (index + 1) % self.__capacity
        return index
