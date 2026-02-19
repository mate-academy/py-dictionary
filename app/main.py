from typing import Any, List


class Dictionary:
    initial_capacity = 8
    load_factor_threshold = 0.7

    def __init__(self) -> None:
        self.list_of_nodes: List[Node | None] = \
            [None for _ in range(Dictionary.initial_capacity)]
        self.length = 0

    def __setitem__(
            self,
            key: Any,
            value: Any
    ) -> None:

        existing_key = self.find_key_in_dict(key)

        if isinstance(existing_key, int):
            self.list_of_nodes[existing_key].value = value
            return

        if (self.__len__() + 1
                > len(self.list_of_nodes) * Dictionary.load_factor_threshold):
            self.extend_list_of_nodes()

        index = self.calculate_index(key)

        if not self.list_of_nodes[index]:
            self.list_of_nodes[index] = Node(key, value)

        else:
            while isinstance(self.list_of_nodes[index].next, int):
                index = self.list_of_nodes[index].next
            self.list_of_nodes[index].next = self.find_empty_cell(index)
            self.list_of_nodes[self.list_of_nodes[index].next] \
                = Node(key, value)

        self.length += 1

    def __getitem__(
            self,
            key: Any
    ) -> Any:

        existing_key = self.find_key_in_dict(key)
        if isinstance(existing_key, int):
            return self.list_of_nodes[existing_key].value
        else:
            raise KeyError(f"The key '{key}' is not present in the dictionary")

    def __len__(self) -> int:
        return self.length

    def calculate_index(
            self,
            key: Any
    ) -> int:

        return abs(hash(key)) % len(self.list_of_nodes)

    def extend_list_of_nodes(self) -> None:
        existing_len = len(self.list_of_nodes)
        self.list_of_nodes.extend(None for _ in range(len(self.list_of_nodes)))

        temporary_list = []
        for i in range(0, existing_len):
            if self.list_of_nodes[i]:
                temporary_list.append(
                    [self.list_of_nodes[i].key,
                     self.list_of_nodes[i].value]
                )
                self.list_of_nodes[i] = None
        self.length = 0
        for item in temporary_list:
            self.__setitem__(item[0], item[1])

    def find_key_in_dict(
            self,
            key: Any,
            *next_index: int
    ) -> int | None:

        if next_index:
            index = next_index[0]
        else:
            index = self.calculate_index(key)

        if self.list_of_nodes[index]:
            if (self.list_of_nodes[index].hash == hash(key)
                    and self.list_of_nodes[index].key == key):
                return index

            elif isinstance(self.list_of_nodes[index].next, int):
                return self.find_key_in_dict(
                    key,
                    self.list_of_nodes[index].next
                )

    def find_empty_cell(
            self,
            index: int
    ) -> int:

        for i in range(index, len(self.list_of_nodes)):
            if not self.list_of_nodes[i]:
                return i

        for i in range(0, index):
            if not self.list_of_nodes[i]:
                return i


class Node:
    def __init__(
            self,
            key: Any,
            value: Any
    ) -> None:

        self.key = key
        self.value = value
        self.hash = hash(key)
        self.next = None
