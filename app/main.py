from typing import Any


class Dictionary:
    def __init__(self, *args) -> None:
        self.hash_table = None
        self.capacity = 8
        self.load_factor = 2 / 3
        self.reinit(args)

    def reinit(self, args: list) -> None:
        while len(args) > self.capacity * self.load_factor:
            self.capacity *= 2
        self.hash_table = [[] for i in range(self.capacity)]
        for key_value in args:
            key, value = key_value
            index = hash(key) % self.capacity
            hash_node = self.hash_table[index]
            while len(hash_node) != 0:
                index = (index + 1) % self.capacity
                hash_node = self.hash_table[index]
            hash_node.append([hash(key), key, value])

    def __setitem__(self, key: Any, value: Any) -> None:
        if len(self) + 1 > self.capacity * self.load_factor:
            reinit_args = []
            for node in self.hash_table:
                if len(node) != 0:
                    reinit_args.append((node[0][1], node[0][2]))
            self.reinit(list(reinit_args))
        index = hash(key) % self.capacity
        hash_node = self.hash_table[index]
        while len(hash_node) != 0:
            if hash_node[0][1] == key:
                hash_node[0][2] = value
                break
            index = (index + 1) % self.capacity
            hash_node = self.hash_table[index]
        hash_node.append([hash(key), key, value])

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity
        hash_node = self.hash_table[index]
        while len(hash_node) != 0:
            try:
                if hash_node[0][0] == hash(key) and hash_node[0][1] == key:
                    return hash_node[0][2]
            except KeyError as error:
                raise error
            index = (index + 1) % self.capacity
            hash_node = self.hash_table[index]
        raise KeyError

    def __len__(self) -> int:
        result = sum(bool(node) for node in self.hash_table)
        return result
