from decimal import Decimal

from typing import Any
from app.point import Point


class Dictionary:
    def __inc_cell(self, _cell: int) -> int:
        cell = _cell
        if cell == self.len_hash_table - 1:
            cell = 0
        else:
            cell += 1
        return cell

    def __check_len(self, key: Any) -> None:
        part_value = int(self.len_hash_table * 2 / 3)
        if hash(key) % self.len_hash_table > self.len_hash_table:
            self.len_hash_table += part_value
        if self.__len__() >= part_value:
            self.len_hash_table += part_value
            new_hash_table = [[None, None] for _ in range(self.len_hash_table)]
            for each in self.hash_table:
                if each[0] is not None:
                    new_cell = hash(each[0]) % self.len_hash_table
                    new_hash_table[new_cell][0] = each[0]
                    new_hash_table[new_cell][1] = each[1]
            self.hash_table = new_hash_table

    def __setitem__(self, key: Any, value: Any) -> None:
        #print("__setitem__")
        cell = hash(key) % self.len_hash_table
        while True:
            if self.hash_table[cell][0] is not None:
                if self.hash_table[cell][0] == key:
                    self.__check_len(key)
                    self.hash_table[cell][1] = value
                    break
                else:
                    cell = self.__inc_cell(cell)
            else:
                self.__check_len(key)
                self.hash_table[cell][0] = key
                self.hash_table[cell][1] = value
                break
                

    def __getitem__(self, key: Any) -> Any:
        print("__getitem__")
        # Starting point
        cell = hash(key) % self.len_hash_table
        # First key check just in case
        print("Given key:", key)
        if isinstance(key, Point):
            print("x:", key.x)
            print("y:", key.y)
            print("hash:", hash((key.x, key.y)))
            print("Cell:", hash((key.x, key.y)) % self.len_hash_table)
        print("Picked key:", self.hash_table[cell][0])
        if self.hash_table[cell][0] != key:
            starting_point = cell
            while True:
                cell = self.__inc_cell(cell)
                if cell == starting_point:
                    raise KeyError
                if self.hash_table[cell][0] == key:
                    break
        return self.hash_table[cell][1]

    def __len__(self) -> int:
        num = 0
        for i in self.hash_table:
            if i[0] != None:
                num += 1
        return num

    def __init__(self) -> None:
        self.hash_table = [[None, None] for _ in range(8)]
        self.len_hash_table = 8
