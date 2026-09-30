from typing import Any


class Dictionary:
    _DELETED = object()

    def __init__(self,
                 key: Any = None,
                 value: Any = None,
                 ) -> None:
        self.slots = 8
        self.key = key
        self.value = value
        self.hash_table = [None] * self.slots
        self.length = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        self._resize()
        return self.set_item(key, value)

    def __getitem__(self, key: Any) -> Any:
        ind = self._find(key)
        if ind is None:
            raise KeyError(key)
        return self.hash_table[ind][2]

    def __len__(self) -> int:
        return self.length

    def get_hash(self, key: Any) -> int:
        return hash(key) % len(self.hash_table)

    def capacity(self) -> int:
        x = self.__len__()
        y = self.slots
        if x != 0:
            return x / y
        elif x == 0 or x is None:
            return 0

    def _find(self, key: Any) -> None | int:
        ind = self.get_hash(key)
        while self.hash_table[ind] is not None:
            if (self.hash_table[ind] is not self._DELETED
                    and self.hash_table[ind][0] == key):
                return ind
            ind = (ind + 1) % len(self.hash_table)
        return None

    def _resize(self) -> None:
        cap = self.capacity()
        old_hash_table = self.hash_table
        if cap >= 0.67:
            self.slots *= 2
            self.hash_table = [None] * self.slots
            self.length = 0
            for elem in old_hash_table:
                if elem is not None and elem is not self._DELETED:
                    self.set_item(elem[0], elem[2])

    def set_item(self, key: Any, value: Any) -> None:
        ind = self.get_hash(key)
        first_free = None
        while self.hash_table[ind] is not None:
            if self.hash_table[ind] is self._DELETED:
                if first_free is None:
                    first_free = ind
            elif self.hash_table[ind][0] == key:
                self.hash_table[ind] = (key, ind, value)
                return
            ind = (ind + 1) % len(self.hash_table)
        target = first_free if first_free is not None else ind
        self.hash_table[target] = (key, target, value)
        self.length += 1

    def __delitem__(self, key: Any) -> None:
        ind = self._find(key)
        if ind is None:
            raise KeyError(key)
        self.hash_table[ind] = self._DELETED
        self.length -= 1
