from dataclasses import dataclass
from collections.abc import Hashable
from copy import deepcopy
from typing import Any


@dataclass
class Element:
    key: Hashable
    hash: int
    value: Any


class Dictionary:
    LOAD_FACTOR = 2 / 3

    def __init__(self, **kwargs: Any) -> None:
        self.__capacity = 8
        self.__slots: list[None | Element] = [None] * self.__capacity
        self.__new_slots = []
        self.__count_not_none_elem = 0

        for key, value in kwargs.items():
            self[key] = value


    def __setitem__(self, key: Hashable, value: Any) -> None:
        key_exist = any(key == elem.key for elem in self.__slots if elem)
        if self.__count_not_none_elem + 1 > int(self.__capacity * self.LOAD_FACTOR) and not key_exist:
            self.resize_table()
            self.__slots = deepcopy(self.__new_slots)
            self.__new_slots.clear()

        self.set_place(key, value, self.__slots)

    def set_place(self, key: Hashable, value: Any, list_of_slots: list) -> None:
        place_dependent_on_hash = hash(key) % self.__capacity
        while True:
            if not list_of_slots[place_dependent_on_hash] or list_of_slots[place_dependent_on_hash].key == key:
                self.__count_not_none_elem += 1 if list_of_slots is self.__slots  and not list_of_slots[place_dependent_on_hash] else 0
                list_of_slots[place_dependent_on_hash] = Element(
                    key=key,
                    value=value,
                    hash=hash(key)
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

    def count_not_none_elem(self) -> int:
        return sum(1 for elem in self.__slots if elem)

    def __getitem__(self, key: Hashable) -> Any:
        pass


d = Dictionary(solo=1, duo=2)
d[1] = "123"
d[2] = "456"
d[2] = "789"
d[12] = "qwe"
d[4] = "rty"
d[6] = "zxc"
d[1] = "jkl"
d[9] = "asd"
print