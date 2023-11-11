from __future__ import annotations
if __name__ == "__main__":
    from point import Point


class Dictionary:
    def __init__(self) -> None:
        self._capacity = None
        self._threshold = None
        self._load_factor = None
        self._data = None

        self.clear()

    def clear(self) -> None:
        self._capacity = 8
        self._threshold = int(self._capacity * (2 / 3))
        self._load_factor = 0
        self._data = [None] * self._capacity

    def _find_cell_by_key(self, key: object) -> tuple(bool, object):
        hash_key = hash(key)
        hash_cell = hash_key % self._capacity
        while True:
            if self._data[hash_cell] is None:
                return False, hash_cell, hash_key,
            elif self._data[hash_cell][0] == key:
                return True, hash_cell, hash_key,
            else:
                hash_cell += 1
                if hash_cell == self._capacity:
                    hash_cell = 0

    def __setitem__(self, key: object, value: object) -> None:
        found_key, cell_key, hash_key = self._find_cell_by_key(key)
        if found_key:
            self._data[cell_key][2] = value
        else:
            self._data[cell_key] = [key, hash_key, value]
            self._load_factor += 1
            self.resize_data()

    def set(self, key: object, value: object) -> None:
        self.__setitem__(key, value)

    def __getitem__(self, key: object) -> object:
        found_key, cell_key, _ = self._find_cell_by_key(key)
        if found_key:
            return self._data[cell_key][2]
        else:
            raise KeyError(f"Class Dictionary: can't find key{key}")

    def get(self, key: object, default: object = None) -> object:
        found_key, cell_key, _ = self._find_cell_by_key(key)
        if found_key:
            return self._data[cell_key][2]
        else:
            return default

    def __len__(self) -> int:
        return self._load_factor

    def __delitem__(self, key: object) -> None:
        found_key, cell_key, _ = self._find_cell_by_key(key)
        if found_key:
            self._data[cell_key] = None
            self._load_factor -= 1
        else:
            raise KeyError(f"Class Dictionary: can't find key{key}")

    def pop(self, key: object, *args) -> object:
        found_key, cell_key, _ = self._find_cell_by_key(key)
        if found_key:
            value = self._data[cell_key][2]
            self._data[cell_key] = None
            self._load_factor -= 1
            self.rebuild_data()
            return value
        elif args:
            return args[0]
        else:
            raise KeyError(f"Class Dictionary: can't find key{key}")

    def __iter__(self) -> object:
        data = self._data
        for element in data:
            if element is not None:
                yield element[0], element[2]

    def update(self, other: object) -> None:
        if isinstance(other, list):
            for dictionary in other:
                for key, value in dictionary:
                    self.__setitem__(key, value)
        elif isinstance(other, Dictionary):
            for key, value in other:
                self.__setitem__(key, value)
        else:
            self.__setitem__(other, None)

    def resize_data(self) -> None:
        if self._load_factor > self._threshold:
            data = self._data
            self._capacity *= 2
            self._threshold = int(self._capacity * (2 / 3))
            self._load_factor = 0
            self._data = [None] * self._capacity

            for element in data:
                if element is not None:
                    self.__setitem__(element[0], element[2])

    def rebuild_data(self) -> None:
        data = self._data
        self._load_factor = 0
        self._data = [None] * self._capacity

        for element in data:
            if element is not None:
                self.__setitem__(element[0], element[2])


if __name__ == "__main__":
    print("Test started")
    point = None
    dictionary1 = Dictionary()
    dictionary2 = Dictionary()
    for index in range(50):
        point = Point(index, index)
        dictionary1[point] = index
    for index in range(50):
        point = Point(index ** 2, index ** 2)
        dictionary2.set(point, index)

    for key, value in dictionary1:
        print(f"Key:{key}, Value:{value}")

    for key, value in dictionary1:
        print(f"Value:{dictionary1[key]}")

    print(len(dictionary1))

    dictionary1.update(Point(1000, 1000))
    print(len(dictionary1))

    dictionary1.update(dictionary2)
    print(len(dictionary1))

    dictionary1.update([dictionary1, dictionary2])
    print(len(dictionary1))

    key_list = []
    for key, value in dictionary2:
        key_list.append(key)
    for key in key_list:
        print(dictionary1.pop(key))
        print(len(dictionary1))
    print(len(dictionary1))

    for i in range(10):
        print(dictionary1.get(i, i**5))

    dictionary1.clear()
    print(len(dictionary1))

    try:
        dictionary1["missing_key"]
    except KeyError as error:
        print(error)

    print("All tests finished")
