from __future__ import annotations


class Dictionary:
    def __init__(self) -> None:
        self.objects = []
        self.capacity = 8
        self.load_factor = 3 / 2

        self.iter_counter = 0

    def __len__(self) -> int:
        return len(self.objects)

    def clear(self) -> None:
        self.objects = []

    def __setitem__(self, key: str, value: str) -> None:
        try:

            if len(self.objects) == 0:
                self.objects.append([key, value, hash(key)])
            for index in range(len(self.objects)):
                if self.objects[index][0] == key:
                    self.objects[index] = [key, value, hash(key)]
                    break
                else:
                    if index == len(self.objects) - 1:
                        self.objects.append([key, value, hash(key)])
        except Exception(KeyError):
            raise KeyError

    def __getitem__(self, item: str) -> None | str:
        for element in self.objects:
            if element[0] == item:
                return element[1]
        raise KeyError

    def __delitem__(self, index: int) -> None:
        self.objects.pop(index)

    def get(self, index: str) -> None | str:
        return self.__getitem__(index)

    def pop(self, index: int = None) -> str:
        if index is None:
            value = self.objects[-1][1]
            self.objects.pop()
            return value
        value = self.objects[index][1]
        self.objects.pop(index)
        return value

    def update(self, pair: dict) -> None:
        key = [key for key in pair][0]
        value = pair[key]

        for index in range(len(self.objects)):
            if self.objects[index][0] == key:
                self.objects[index] = [key, value, hash(key)]
                break
            else:
                if index == len(self.objects) - 1:
                    self.objects.append([key, value, hash(key)])
