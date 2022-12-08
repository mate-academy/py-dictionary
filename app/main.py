from copy import copy
from dataclasses import dataclass
from typing import Any, Union


@dataclass
class Dictionary:
    def __init__(self) -> None:
        self.size = 8
        self.load = 0
        self.length = 0
        self.nodes = [[] for i in range(self.size)]

    def resize(self) -> None:
        temp = copy(self.nodes)
        self.load = 0
        self.length = 0
        self.size = 2 * self.size
        self.nodes = [[] for i in range(self.size)]
        for node in temp:
            for item in node:
                if item:
                    self.__write(item[0], item[1])

    def __setitem__(self,
                    key: Union[int, float, bool, str, tuple],
                    value: Any) -> None:
        if self.load > 2 / 3 * self.size:
            self.resize()
        self.__write(key, value)

    def __write(self,
                key: Union[int, float, bool, str, tuple],
                value: Any) -> None:
        write = True
        for item in self.nodes[hash(key) % self.size]:
            if key in item:
                item[1] = value
                write = False
                break
        if write:
            self.length += 1
            if not self.nodes[hash(key) % self.size]:
                self.load += 1
            self.nodes[hash(key) % self.size].append([key, value])

    def __getitem__(self,
                    key: Union[int,
                               float,
                               bool,
                               str,
                               tuple]) -> Union[Any, KeyError]:
        for node in self.nodes[hash(key) % self.size]:
            if key in node:
                return node[1]
        raise KeyError

    def __len__(self) -> int:
        return self.length

    def clear(self) -> None:
        self.size = 8
        self.load = 0
        self.length = 0
        self.nodes = [[] for i in range(self.size)]

    def __delitem__(self, key: Any) -> Union[None, KeyError]:
        for node in self.nodes[hash(key) % self.size]:
            if key in node:
                self.nodes[hash(key) % self.size].remove(node)
                self.length -= 1
            else:
                raise KeyError

    def get(self, key: Union[int, float, bool, str, tuple]) -> Any:
        for node in self.nodes[hash(key) % self.size]:
            if key in node:
                return node[1]

    def pop(self, key: Union[int, float, bool, str, tuple]) -> Any:
        for node in self.nodes[hash(key) % self.size]:
            if key in node:
                temp_value = copy(node[1])
                self.nodes[hash(key) % self.size].remove(node)
                self.length -= 1
                return temp_value

    def update(self, other: Any) -> None:
        for node in other.nodes:
            for item in node:
                if item:
                    self.__setitem__(item[0], item[1])

    def __repr__(self) -> str:
        temp_lst = []
        for node in self.nodes:
            for item in node:
                if item:
                    temp_lst.append(f"{item[0]}: {item[1]}")
        result = ", ".join(it for it in temp_lst)
        return f"{{{result}}}"
