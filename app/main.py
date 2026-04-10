from dataclasses import dataclass
from collections.abc import Hashable
from typing import Any, Generator


@dataclass
class Element:
    key: Hashable
    key_hash: int
    value: Any


class Dictionary:
    LOAD_FACTOR = 2 / 3

    def __init__(self, **kwargs: Any) -> None:
        self.__capacity = 8
        self.__slots: list[None | Element | bool] = [None] * self.__capacity
        self.__new_slots = []
        self.__existing_keys = set()

        for key, value in kwargs.items():
            self[key] = value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if (len(self.__existing_keys) + 1
                > int(self.__capacity * self.LOAD_FACTOR) and key not in self.__existing_keys):
            self.resize_table()
            self.__slots = self.__new_slots
            self.__new_slots = []

        self.set_place(key, value, self.__slots)

    def set_place(self, key: Hashable, value: Any,
                  list_of_slots: list) -> None:
        place_dependent_on_hash = hash(key) % self.__capacity
        while True:
            if (not list_of_slots[place_dependent_on_hash]
                    or list_of_slots[place_dependent_on_hash].key == key):
                if (list_of_slots is self.__slots
                    and not list_of_slots[place_dependent_on_hash]):
                    self.__existing_keys.add(key)

                list_of_slots[place_dependent_on_hash] = Element(
                    key=key,
                    value=value,
                    key_hash=hash(key)
                )
                break
            else:
                place_dependent_on_hash += 1
                place_dependent_on_hash %= self.__capacity

    def resize_table(self) -> None:
        self.__capacity *= 2
        self.__new_slots: list[None | Element] = [None] * self.__capacity
        for element in self.__slots:
            if element:
                self.set_place(element.key, element.value, self.__new_slots)

    def __getitem__(self, key: Hashable) -> Any:
        place_dependent_on_hash = hash(key) % self.__capacity
        while True:
            if self.__slots[place_dependent_on_hash]:
                if self.__slots[place_dependent_on_hash].key == key:
                    return self.__slots[place_dependent_on_hash].value

                place_dependent_on_hash += 1
                place_dependent_on_hash %= self.__capacity
            elif self.__slots[place_dependent_on_hash] is False:
                place_dependent_on_hash += 1
                place_dependent_on_hash %= self.__capacity
            else:
                raise KeyError("The key does not exist")

    def __len__(self) -> int:
        return len(self.__existing_keys)

    def clear(self) -> None:
        self.__capacity = 8
        self.__slots = [None] * self.__capacity
        self.__existing_keys = set()

    def get(self, key: Hashable, default_value: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default_value

    def update(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            self[key] = value

    def __delitem__(self, key: Hashable) -> None:
        place_dependent_on_hash = hash(key) % self.__capacity
        while True:
            if self.__slots[place_dependent_on_hash]:
                if self.__slots[place_dependent_on_hash].key == key:
                    self.__slots[place_dependent_on_hash] = False
                    self.__existing_keys.remove(key)
                    break

                place_dependent_on_hash += 1
                place_dependent_on_hash %= self.__capacity
            else:
                raise KeyError("The key does not exist")

    def pop(self, key: Hashable) -> Any:
        place_dependent_on_hash = hash(key) % self.__capacity
        while True:
            if self.__slots[place_dependent_on_hash]:
                if self.__slots[place_dependent_on_hash].key == key:
                    element_to_return = (
                        self.__slots[place_dependent_on_hash].value)
                    self.__slots[place_dependent_on_hash] = False
                    self.__existing_keys.remove(key)
                    return element_to_return

                place_dependent_on_hash += 1
                place_dependent_on_hash %= self.__capacity
            else:
                raise KeyError("The key does not exist")

    def __iter__(self) -> Generator:
        return (element.key for element in self.__slots if element)

d = Dictionary(solo=11, duo=22)
d.update(top=1, pot=2)
d[4] = "123"
d[2] = "qwe"
print(len(d))
del d[2]
print(len(d))
d[3] = "456"
print(d.pop(3))
print(len(d))

for i in d:
    print(i)

