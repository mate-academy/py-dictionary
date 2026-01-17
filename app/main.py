from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.keys = set()
        self.nodes = []
        self.nodes.extend([None] * 8)

    def set_cell(self, num_cell: int, key: Any, value: Any) -> None:
        while (isinstance(self.nodes[num_cell], tuple)
               and key != self.nodes[num_cell][0]):
            num_cell += 1
            num_cell %= len(self.nodes)
        self.nodes[num_cell] = (key, value)

    def __setitem__(self, key: Any, value: Any) -> None:
        num_of_not_empty_point = len(self.nodes) - self.nodes.count(None)
        if ((num_of_not_empty_point + 1) / len(self.nodes)
                > 2 / 3 and key not in self.keys):
            self.nodes.extend([None] * len(self.nodes))
            for index, node in enumerate(self.nodes):
                if node is not None:
                    key_new, value_new = node[0], node[1]
                    num_cell_new = hash(node[0]) % len(self.nodes)
                    self.nodes[index] = None
                    self.set_cell(num_cell_new, key_new, value_new)
        self.keys.add(key)
        num_cell = hash(key) % len(self.nodes)
        self.set_cell(num_cell, key, value)

    def __repr__(self) -> str:
        return f"{self.nodes}"

    def __getitem__(self, item: Any) -> Any:
        for node in self.nodes:
            if isinstance(node, tuple):
                if node[0] == item:
                    return node[1]
        raise KeyError

    def __len__(self) -> int:
        return len(self.keys)

    def clear(self) -> None:
        self.nodes, self.keys = list(), set()

    def __delitem__(self, key: Any) -> None:
        for index, node in enumerate(self.nodes):
            if isinstance(node, tuple):
                if key == node[0]:
                    self.nodes[index] = None
                    return
        raise KeyError

    def get(self, key: Any) -> Any:
        for index, node in enumerate(self.nodes):
            if isinstance(node, tuple):
                if key == node[0]:
                    return self.nodes[index][1]
        return None

    def pop(self, key: Any) -> Any:
        for index, node in enumerate(self.nodes):
            if isinstance(node, tuple):
                if key == node[0]:
                    result = self.nodes[index][1]
                    self.nodes[index] = None
                    return result
        raise KeyError

    def update(self, data_to_update: dict) -> None:
        for keys, values in data_to_update.items():
            self.__setitem__(keys, values)

    def __iter__(self) -> Any:
        return iter(
            [node[0] for node in self.nodes if isinstance(node, tuple)]
        )
