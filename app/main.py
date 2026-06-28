from typing import TypeVar, Hashable, Any

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class Node:
    def __init__(self, key: K, value: V) -> None:
        self.key = key
        self.hash = hash(key)
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self.size = 8
        self.count = 0
        self.data = [[] for _ in range(self.size)]

    def resize(self) -> None:
        self.size *= 2
        self.count = 0
        old_data = self.data
        self.data = [[] for _ in range(self.size)]

        for buckets in old_data:
            for node in buckets:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: K, value: V) -> None:
        if self.count / len(self.data) > 0.75:
            self.resize()

        current_hash = hash(key)
        index = current_hash % len(self.data)

        new_node = Node(key, value)
        for node in self.data[index]:
            if node.key == new_node.key:
                node.value = new_node.value
                break
        else:
            self.data[index].append(new_node)
            self.count += 1

    def __getitem__(self, key: K) -> Any:
        current_hash = hash(key)
        index = current_hash % len(self.data)

        for node in self.data[index]:
            if node.hash == current_hash and node.key == key:
                return node.value
        else:
            raise KeyError(key)

    def __len__(self) -> int:
        return self.count

    def clear(self) -> None:
        self.size = 8
        self.count = 0
        self.data = [[] for _ in range(self.size)]

    def __delitem__(self, key: K) -> None:
        current_hash = hash(key)
        index = current_hash % len(self.data)

        for i, node in enumerate(self.data[index]):
            if node.hash == current_hash and node.key == key:
                self.data[index].pop(i)
                self.count -= 1
                return
        else:
            raise KeyError(key)

    def get(self, key: K, default: Any = None) -> Any:
        current_hash = hash(key)
        index = current_hash % len(self.data)

        for node in self.data[index]:
            if node.hash == current_hash and node.key == key:
                return node.value
        else:
            return default

    def pop(self, key: K, default: Any = ...) -> Any:
        current_hash = hash(key)
        index = current_hash % len(self.data)

        for i, node in enumerate(self.data[index]):
            if node.hash == current_hash and node.key == key:
                deleted_value = self.data[index][i].value
                self.data[index].pop(i)
                self.count -= 1
                return deleted_value
        if default is not ...:
            return default
        else:
            raise KeyError(key)

    def __iter__(self) -> Any:
        for node_list in self.data:
            for node in node_list:
                yield node.key

    def update(self, other: Any) -> None:
        for key in other:
            self.__setitem__(key, other[key])
