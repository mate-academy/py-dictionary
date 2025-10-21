from typing import Iterator, Any


class Dictionary:
    def __init__(self, **kwargs) -> None:
        length = len(kwargs)
        self.capacity = 8
        self.load_factor = 2 / 3
        while length > self.capacity * self.load_factor:
            self.capacity *= 2
        self.hash_table = [[] for _ in range(self.capacity)]
        _max_table_index = len(self.hash_table) - 1
        for key, value in kwargs.items():
            ind = hash(key) % self.capacity
            self.add_kwargs_init(
                self.hash_table,
                ind,
                key,
                value,
                _max_table_index
            )

    def __setitem__(self,
                    key: Any,
                    value: Any
                    ) -> None:
        self.capacity = len(self.hash_table)
        temp_capacity = self.capacity
        length = 0
        results = []

        for table in self.hash_table:
            if table:
                results.append(table)
                length += 1

        results.append([key, hash(key), value])
        length += 1

        while length > temp_capacity * self.load_factor:
            temp_capacity *= 2

        if temp_capacity == self.capacity:
            _max_table_index = len(self.hash_table) - 1
            ind = hash(key) % self.capacity
            self.add_kwargs_init(
                self.hash_table,
                ind,
                key,
                value,
                _max_table_index
            )
        else:
            self.capacity = temp_capacity
            self.hash_table = [[] for _ in range(self.capacity)]
            _max_table_index = len(self.hash_table) - 1
            for result in results:
                ind = result[1] % self.capacity
                self.rehash(self.hash_table, ind, result, _max_table_index)

    def __getitem__(self,
                    item: Any
                    ) -> Any:
        self.capacity = len(self.hash_table)
        _max_index = self.capacity - 1
        ind = hash(item) % self.capacity
        if not self.hash_table[ind]:
            raise KeyError

        while True:
            if self.hash_table[ind]:
                if self.hash_table[ind][0] == item:
                    return self.hash_table[ind][2]
                elif ind == _max_index:
                    ind = 0
                    continue
                ind += 1
            else:
                raise KeyError

    def __len__(self) -> int:
        count = 0
        for table in self.hash_table:
            if table:
                count += 1
        return count

    def __delitem__(self,
                    key: Any
                    ) -> None:
        self.capacity = len(self.hash_table)
        ind = hash(key) % self.capacity
        _max_index = self.capacity - 1
        results = []

        if not self.hash_table[ind]:
            raise KeyError

        while True:
            if self.hash_table[ind]:
                if self.hash_table[ind][0] == key:
                    self.hash_table[ind] = []
                    break
                elif ind == _max_index:
                    ind = 0
                    continue
                ind += 1
            else:
                raise KeyError

        for table in self.hash_table:
            if table:
                results.append(table)

        self.hash_table = [[] for _ in range(self.capacity)]
        _max_index = self.capacity - 1

        for result in results:
            ind = result[1] % self.capacity
            self.rehash(self.hash_table, ind, result, _max_index)

    def __iter__(self) -> Iterator[Any]:
        for table in self.hash_table:
            if table:
                yield table[0]

    def items(self) -> Iterator[Any]:
        for table in self.hash_table:
            if table:
                yield table[0], table[2]

    def keys(self) -> Iterator[Any]:
        for table in self.hash_table:
            if table:
                yield table[0]

    def values(self) -> Iterator[Any]:
        for table in self.hash_table:
            if table:
                yield table[2]

    def clear(self) -> None:
        self.capacity = 8
        self.hash_table = [[] for _ in range(self.capacity)]

    def get(self, key: Any, default: Any = None) -> Any:
        self.capacity = len(self.hash_table)
        _max_index = self.capacity - 1
        ind = hash(key) % self.capacity

        if not self.hash_table[ind]:
            return default

        while True:
            if self.hash_table[ind]:
                if self.hash_table[ind][0] == key:
                    return self.hash_table[ind][2]
                elif ind == _max_index:
                    ind = 0
                    continue
                ind += 1
            else:
                return default

    def pop(self, key: Any, default: Any = None) -> Any:
        self.capacity = len(self.hash_table)
        _max_index = self.capacity - 1
        ind = hash(key) % self.capacity
        results = []

        if not self.hash_table[ind]:
            if default is not None:
                return default
            raise KeyError

        while True:
            if self.hash_table[ind]:
                if self.hash_table[ind][0] == key:
                    value_to_return = self.hash_table[ind][2]
                    self.hash_table[ind] = []
                elif ind == _max_index:
                    ind = 0
                    continue
                ind += 1
            else:
                if default is not None:
                    return default
                raise KeyError

        for table in self.hash_table:
            if table:
                results.append(table)

        self.hash_table = [[] for _ in range(self.capacity)]
        _max_index = self.capacity - 1

        for result in results:
            ind = result[1] % self.capacity
            self.rehash(self.hash_table, ind, result, _max_index)

        return value_to_return

    def update(self, other: Any = None, **kwargs) -> None:
        if other is not None:
            if hasattr(other, "items"):
                for key, value in other.items():
                    self[key] = value
            else:
                for key, value in other:
                    self[key] = value

        for key, value in kwargs.items():
            self[key] = value

    @staticmethod
    def add_kwargs_init(hash_table: list,
                        ind: int,
                        key: Any,
                        value: Any,
                        _max_table_index: int
                        ) -> None:
        while True:
            if hash_table[ind]:
                if hash_table[ind][0] == key:
                    hash_table[ind] = [key, hash(key), value]
                    break
                elif ind == _max_table_index:
                    ind = 0
                    continue
                ind += 1
                continue
            else:
                hash_table[ind] = [key, hash(key), value]
                break

    @staticmethod
    def rehash(hash_table: list,
               ind: int,
               result: list,
               _max_table_index: int)\
            -> None:
        while True:
            if hash_table[ind]:
                if hash_table[ind][0] == result[0]:
                    hash_table[ind] = [result[0], result[1], result[2]]
                    break
                elif ind == _max_table_index:
                    ind = 0
                    continue
                ind += 1
                continue
            else:
                hash_table[ind] = [result[0], result[1], result[2]]
                break
