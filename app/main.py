from collections.abc import Hashable, Iterable
from typing import Any

from pprint import pformat


class Dictionary:

    def __init__(self, elements: Iterable=[]) -> None:
        if not isinstance(elements, Iterable):
            raise TypeError(f"Non-iterable type: '{type(elements)}'")
        else:
            self.__load_factor = 0.66  # 2/3
            # Default size of dict is 8
            # Due to the rule, that the dict should expand x2 when 2/3 of it are occupied
            # It should've size on creation, where 2/3 of it will be bigger, than len(elements)
            self.__table_size = 2 ** ((len(elements).bit_length() if len(elements).bit_length() > 2 else 2) + 1)
            self.__buckets = [None, ] * self.__table_size
            self.__occupied = 0
            self.__assign_elements(elements)


    def __table_resizing(self, new_size: int | float) -> None:
        temp_buckets = [bucket for bucket in self.__buckets if bucket]
        self.__occupied = len(temp_buckets)
        self.__table_size *= new_size
        self.__buckets = [(), ] * self.__table_size
        self.__assign_elements(temp_buckets)


    def __assign_elements(self, elements: tuple) -> None:
        """
        This function checks, if element meets the formatting criteria
        and updates the amount of occupied cells in table.
        If occupied > 2/3 of size of the table - it calls resizing function
        """
        for element in elements:
            if element and len(element) != 2:
                raise ValueError("Can't insert the element", element, "due to it's incorrect format.")
            else:
                self.__setitem__(element[0], element[1])
                if element:
                    self.__occupied += 1
                if self.__occupied >= (self.__table_size * self.__load_factor):
                    self.__table_resizing(2)



    def __setitem__(self, key: Hashable, value: Any) -> None:
        """
        This function checks, if the key is hashable and looks for an empty cell in the table.
        It starts from index, derived from key's hash, and, as a collision resolution method,
        if it reaches the limit of the table and still not did its job - starts from 0
        The "lap" variable is used to avoid infinite loops. It'll resize the table if something will go wrong.
        """
        if not isinstance(key, Hashable):
            raise TypeError(f"Unhashable key {key}")
        hashed_value = hash(key)
        index = hashed_value % self.__table_size
        lap = 0
        while lap < 2:
            if not self.__buckets[index]:
                self.__buckets[index] = (key, value)
                break
            else:
                index += 1
                if index >= self.__table_size:
                    index = 0
                    lap += 1
            # If program reached this place - it means that something went wrong.
            self.__table_resizing(2)
            self.__setitem__(key, value)

    def __getitem__(self, key: Hashable) -> Any:
        if not isinstance(key, Hashable):
            raise TypeError(f"Unhashable key {key}")
        hashed_value = hash(key)
        index = hashed_value % self.__table_size
        lap = 0
        while lap < 2:
            if self.__buckets[index] and key == self.__buckets[index][0]:
                return self.__buckets[index][1]
            elif self.__buckets[index] and key != self.__buckets[index][0]:
                raise KeyError("No such key")
            else:
                index += 1
                if index >= self.__table_size:
                    index = 0
                    lap += 1
        raise KeyError("No such key")

    def __len__(self) -> int:
        return self.__occupied

    def __repr__(self) -> str:
        res = "{"
        for pair in self.__buckets:
            if pair:
                res += f"({pair[0]} : {pair[1]})"
        return res + "}"

# def __delitem__(self, key: Hashable) -> None:
#     if key in self.keys:
#         indx = self.keys.index(key)
#         del self.keys[indx]
#         del self.values[indx]
#     else:ror("No such key")

if __name__ == "__main__":
    pass
