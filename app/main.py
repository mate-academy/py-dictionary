from typing import Any


class Dictionary:
    element_count = 0

    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.dict = [[] for _ in range(self.capacity)]
        self.element_count = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        _hash = hash(key)
        number_pucket = _hash % self.capacity
        if self.dict[number_pucket]:
            for val_ue in self.dict[number_pucket]:
                if val_ue[0] == key:
                    val_ue[1] = value
                    return
            self.dict[number_pucket].append([key, value])
            self.element_count += 1
        else:
            self.dict[number_pucket].append([key, value])
            self.element_count += 1

    def __getitem__(self, key: Any) -> Any:
        _hash = hash(key)
        bucket = _hash % self.capacity
        for stored_key, stored_value in self.dict[bucket]:
            if stored_key == key:
                return stored_value
        raise KeyError(key)

    def __len__(self) -> int:
        return self.element_count
