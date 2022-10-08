class Point:
    def __init__(self, first_value: int, second_value: int) -> None:
        self._first_value = first_value
        self._second_value = second_value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return False
        return self.first_value == other.first_value and \
            self.second_value == other.second_value

    def __hash__(self) -> int:
        # Change the implementation of the hash to debug your code.
        # For example, you can return self.x + self.y as a hash
        # which is NOT a best practice, but you will be able to predict
        # a hash value by coordinates of the point and its index
        # in the hashtable as well
        return hash((self.first_value, self.second_value))

    @property
    def first_value(self) -> int:
        return self._first_value

    @property
    def second_value(self) -> int:
        return self._second_value
