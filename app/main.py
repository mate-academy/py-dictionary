from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.length = 0      # in any (add / del item) - change self.length
        self.capacity = 8
        self.loadfactor = 2 / 3
        self.hash_table: list = [None] * 8

    def __setitem__(self, key: Any | Hashable, value: Any) -> None:
        hash_key = self.get_hash(key)
        hash_index = hash_key % len(self.hash_table)
        set_node = (key, hash_key, value)

        if self.hash_table[hash_index] is None:
            self.hash_table[hash_index] = [set_node]
            self.length += 1
        else:
            for node_index, node in enumerate(self.hash_table[hash_index]):
                if key == node[0]:  # [0]- node key
                    self.hash_table[hash_index][node_index] = set_node
                    break
            else:
                self.hash_table[hash_index].append(set_node)
                self.length += 1

        if self.need_resize():
            self.resize_hash_table()

    def __getitem__(self, key: Any | Hashable) -> Any:
        return self.read_item(key, is_del=False, is_raise=True)

    def get(self, key: Any | Hashable, default: Any = None) -> Any:
        return self.read_item(key, default, is_del=False, is_raise=False)

    def __delitem__(self, key: Any | Hashable) -> None:
        return self.read_item(key, is_del=True, is_raise=True)

    def pop(self, key: Any | Hashable, *args) -> Any:
        if args:
            return self.read_item(key,
                                  default=args[0], is_del=True, is_raise=False)
        else:
            return self.read_item(key, is_del=True, is_raise=True)

    def read_item(self,
                  key: Any | Hashable,
                  default: Any = None,
                  is_del: bool = False,
                  is_raise: bool = True
                  ) -> Any:
        hash_key = self.get_hash(key)
        hash_index = hash_key % len(self.hash_table)

        if self.hash_table[hash_index] is not None:
            for node_index, (node_key, node_hash_key, node_val) \
                    in enumerate(self.hash_table[hash_index]):
                if key == node_key and hash_key == node_hash_key:
                    if is_del:
                        self.hash_table[hash_index].pop(node_index)
                        self.length -= 1
                    return node_val

        if is_raise:
            raise KeyError(f"Index '{key}' not found")
        else:
            return default

    def resize_hash_table(self) -> None:
        self.capacity *= 2
        new_hash_table: list = [None] * self.capacity

        for bucket in self.hash_table:
            if bucket is not None:
                for node in bucket:                      # (key, hash_key, val)
                    hash_index = node[1] % len(new_hash_table)  # [1]- hash_key
                    if new_hash_table[hash_index] is None:
                        new_hash_table[hash_index] = [node]
                    else:
                        new_hash_table[hash_index].append(node)
        self.hash_table = new_hash_table

    def need_resize(self) -> bool:
        return self.length > self.capacity * self.loadfactor

    @staticmethod
    def get_hash(value: Any) -> int | bool:
        try:
            return hash(value)
        except Exception :
            raise TypeError(f"Object '{value}' hasn't hash")

    def __len__(self) -> int:
        return self.length

    def __repr__(self) -> str:
        res = ""
        for bucket in self.hash_table:
            if bucket is not None:
                for (node_key, node_hash_key, node_val) in bucket:
                    res += "{" + f"{node_key}: {node_val}" + "}, "
        res = ((f"{self.__class__} | "
               f"len= {self.length} / cap= {self.capacity} | ")
               + res[:-2] + "\n")
        return res

    def clear(self) -> None:
        self.__init__()

    def update(self, pairs_list: list[(Any, Any)]) -> None:
        for (key, value) in pairs_list:
            self.__setitem__(key, value)

    def __iter__(self) -> None:
        for bucket in self.hash_table:
            if bucket is not None:
                for (node_key, _, _) in bucket:     # (key, hash_key, val)
                    yield node_key
