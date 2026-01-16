from typing import Any


# class Iterator:
#     def __init__(self, elements: list):
#         self.elements = elements
#
#     def __iter__(self):
#         self.index = 0
#         return self
#
#     def __next__(self):
#         if self.index == len(self.elements):
#             raise StopIteration
#         result = self.elements[self.index]
#         self.index += 1
#         return result
#
class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(self.key)


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.resized_factor = 2
        self.threshold = int(self.capacity * self.load_factor)
        self.hash_table = [None for _ in range(self.capacity)]

    def __len__(self) -> int:
        result = 0
        for index in range(len(self.hash_table)):
            if self.hash_table[index]:
                result += 1
        return result

    def check_for_resize(self) -> None:
        if len(self) == self.threshold:
            old_hash_table = self.hash_table.copy()
            self.capacity *= self.resized_factor
            self.threshold = int(
                self.capacity * self.load_factor
            )
            self.hash_table = [None for _ in range(self.capacity)]

            for element in old_hash_table:
                if element:
                    index = element.hash % self.capacity
                    if self.hash_table[index]:
                        while self.hash_table[index] is not None:
                            index += 1
                            index %= self.capacity
                    self.hash_table[index] = element

    def __setitem__(self, key: Any, value: Any) -> None:
        replacement = self.change_value(key, value)
        if replacement:
            return
        self.check_for_resize()
        element = Node(key, value)
        index = element.hash % self.capacity
        if self.hash_table[index]:
            while self.hash_table[index] is not None:
                index += 1
                index %= self.capacity
        self.hash_table[index] = element

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity
        while True:
            if self.hash_table[index] is None:
                raise KeyError
            elif self.hash_table[index].key == key:
                return self.hash_table[index].value
            index += 1
            index %= self.capacity

    def change_value(self, key: Any, value: Any) -> bool:
        index = hash(key) % self.capacity
        while self.hash_table[index] is not None:
            if self.hash_table[index].key == key:
                self.hash_table[index].value = value
                return True
            else:
                index += 1
                index %= self.capacity
        return False

# -----------------------------------------------------------------
#     def clear(self):
#         self.hash_table = [None for _ in range(self.capacity)]
#
#     def __delitem__(self, key: Any) -> None:
#         index = hash(key) % self.capacity
#         while True:
#             if self.hash_table[index] is None:
#                 raise KeyError
#             elif self.hash_table[index].key == key:
#                 self.hash_table[index] = None
#                 return
#             else:
#                 index += 1
#                 index %= self.capacity
#
#     def get(self, key: Any):
#         try:
#             result = self[key]
#             return result
#         except KeyError:
#             pass
#
#     def pop(self, key: Any) -> Any:
#         index = hash(key) % self.capacity
#         while True:
#             if self.hash_table[index] is None:
#                 raise KeyError
#             elif self.hash_table[index].key == key:
#                 deleted_value = self.hash_table[index].value
#                 self.hash_table[index] = None
#                 return deleted_value
#             else:
#                 index += 1
#                 index %= self.capacity
#
#     # def update(self):
#     #     pass
#
#     def __iter__(self):
#         result = Iterator(
#           [element.key for element in self.hash_table if element]
#         )
#         iter(result)
#         return result
#
#
#
# items = [
#     (1.1, "one"), (2.2, "two"), (3.3, "tree"),
#     (4.4, "four"), (4.5, "four"), (4.6, "four"), (4.7, "four")
# ]
#
# dictionary = Dictionary()
# for key, value in items:
#     dictionary[key] = value
#
# for element in dictionary:
#     print(element)
#
# print(dictionary.hash_table)
# print(dictionary.pop(1.1))
# print(dictionary.hash_table)
