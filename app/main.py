from typing import Any, List, Optional


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, Point)
                and self.x == other.x and self.y == other.y)

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity: int = capacity
        self.buckets: List[List[Node]] = [[] for _ in range(capacity)]
        self.size: int = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        index = hash(key) % self.capacity
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                node.value = value
                return

        bucket.append(Node(key, value))
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                return node.value

        raise KeyError(key)

    def get(self, key: Any, default: Optional[Any] = None) -> Any:
        index = hash(key) % self.capacity
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                return node.value

        return default

    def __contains__(self, key: Any) -> bool:
        index = hash(key) % self.capacity
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                return True

        return False

    def keys(self) -> List[Any]:
        all_keys: List[Any] = []
        for bucket in self.buckets:
            for node in bucket:
                all_keys.append(node.key)
        return all_keys

    def __len__(self) -> int:
        return self.size


if __name__ == "__main__":
    d = Dictionary()
    p1 = Point(1, 2)
    p2 = Point(3, 4)
    p3 = Point(0, 0)

    d[p1] = "A"
    d[p2] = "B"

    print("Get p1:", d.get(p1))  # A
    print("Get p2:", d.get(p2))  # B
    print("Get missing:", d.get(p3, "Not found"))  # Not found

    print("Contains p1:", p1 in d)  # True
    print("Contains p3:", p3 in d)  # False

    print("All keys:", d.keys())  # [Point(1, 2), Point(3, 4)]
    print("Length:", len(d))  # 2
