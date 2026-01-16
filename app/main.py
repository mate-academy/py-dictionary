from typing import Any


class Dictionary(object):

    def __init__(self, size: int = 1000) -> None:
        self.storage = [[] for _ in range(size)]
        self.size = size
        self.length = 0

    def __setitem__(self, key: str, value: Any) -> None:
        storage_idx = hash(key) % self.size
        for elem in self.storage[storage_idx]:
            if key == elem[0]:
                elem[1] = value
                break
        else:
            self.storage[storage_idx].append([key, value])
            self.length += 1

    def __getitem__(self, key: str) -> Any:
        storage_idx = hash(key) % self.size
        for elem in self.storage[storage_idx]:
            if elem[0] == key:
                return elem[1]

        raise KeyError("Key {} dont exist".format(key))

    def __delitem__(self, key: str) -> None:
        storage_idx = hash(key) % self.size
        for sub_lst in self.storage[storage_idx]:
            if key == sub_lst[0]:
                self.storage[storage_idx].remove(sub_lst)
                self.length -= 1
                return

            raise KeyError("Key {} dont exist".format(key))

    def __contains__(self, key: str) -> bool:
        storage_idx = hash(key) % self.size
        for item in self.storage[storage_idx]:
            if item[0] == key:
                return True
        return False

    def __len__(self) -> int:
        return self.length

    def __iterate_kv(self) -> iter:
        for sub_lst in self.storage:
            if not sub_lst:
                continue
            for item in sub_lst:
                yield item

    def __iter__(self) -> iter:
        for key_var in self.__iterate_kv():
            yield key_var[0]

    def keys(self) -> iter:
        return self.__iter__()

    def values(self) -> iter:
        for key_var in self.__iterate_kv():
            yield key_var[1]

    def items(self) -> iter:
        return self.__iterate_kv()

    def get(self, key: str) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return None

    def __str__(self) -> str:
        res = []
        for elem in self.storage:
            for key_value in elem:
                if isinstance(key_value[0], str):
                    key_str = "\'{}\'".format(key_value[0])
                else:
                    key_str = "{}".format(key_value[0])
                if isinstance(key_value[1], str):
                    value_str = "\'{}\'".format(key_value[1])
                else:
                    value_str = "{}".format(key_value[1])

                res.append("{}: {}".format(key_str, value_str))
        key_value_pairs_str = "{}".format(", ".join(res))
        return "{" + key_value_pairs_str + "}"

    def __repr__(self) -> str:
        return self.__str__()
