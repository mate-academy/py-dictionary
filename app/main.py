from typing import Any, List, Tuple

Chain = List[Tuple[Any, Any]]


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.count_elements = 0
        self.sheet = [[] for _ in range(capacity)]
        self.threshold = 2 / 3

    def __setitem__(self, key: Any, value: Any) -> None:
        index_new_element = hash(key) % self.capacity
        chain = self.sheet[index_new_element]
        for i, (k, v) in enumerate(chain):
            if k == key:
                chain[i] = (key, value)
                return
        chain.append((key, value))
        self.count_elements += 1
        if self.count_elements / self.capacity > self.threshold:
            self._resize()

    def _resize(self) -> None:
        self.capacity *= 2
        old_table = self.sheet
        self.sheet = [[] for _ in range(self.capacity)]

        for element in old_table:
            for k, v in element:
                new_index = hash(k) % self.capacity
                self.sheet[new_index].append((k, v))

    def __len__(self) -> int:
        return self.count_elements

    def __getitem__(self, key: Any) -> Any:
        new_index = hash(key) % self.capacity
        chain = self.sheet[new_index]
        for k, v in chain:
            if k == key:
                return v
        raise KeyError(f"Key '{key}' do not found in the dictionary")
