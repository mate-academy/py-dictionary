from dataclasses import dataclass
from collections.abc import Hashable
from copy import deepcopy
from typing import Any


class Dictionary:
    LOAD_FACTOR = 2 / 3

    def __init__(self):
        self.__capacity = 8
        self.__slots: list[None | Element]= [None] * self.__capacity
        self.__new_slots = []
        self.__count_not_none_elem = 0

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self.set_place(key, value, self.__slots)


    def set_place(self, key: Hashable, value: Any, list_of_slots: list) -> None:
        place_dependent_on_hash = hash(key) % self.__capacity
        while True:
            if not list_of_slots[place_dependent_on_hash]:
                self.__count_not_none_elem += 1
                if self.count_not_none_elem() > int(self.__capacity * self.LOAD_FACTOR):
                    self.resize_table()
                    self.__slots = deepcopy(self.__new_slots)
                    self.__new_slots.clear()

                list_of_slots[place_dependent_on_hash] = Element(
                    key=key,
                    value=value,
                    hash=hash(key)
                )
                break
            elif list_of_slots[place_dependent_on_hash].key == key:
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


@dataclass
class Element:
    key: Hashable
    hash: int
    value: Any

