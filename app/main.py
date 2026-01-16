from typing import Any, Union


class Dictionary:
    def __init__(self) -> None:

        self.current_len_of_dict = 0

        self.initial_capacity = 8

        self.load_factor = 2 / 3

        self.threshold = round(self.load_factor * self.initial_capacity)

        self.hash_table = [[] for i in range(self.initial_capacity)]

    def resize(self) -> None:
        self.initial_capacity *= 2
        self.threshold = round(self.load_factor * self.initial_capacity)
        self.current_len_of_dict = 0
        prev_hash_table = self.hash_table.copy()
        self.hash_table = [[] for i in range(self.initial_capacity)]

        for cell in prev_hash_table:
            if cell:
                for key, value, hash_k in cell:
                    hash_key = hash(key)
                    index = hash_key % self.initial_capacity
                    self.hash_table[index].append((key, value, hash_key))
                    self.current_len_of_dict += 1

    def __setitem__(
            self,
            input_key: Union[int, float, str, object],
            input_value: Any
    ) -> None:
        """ Set self[key] to value. """

        if self.current_len_of_dict >= self.threshold:

            self.resize()

        if self.current_len_of_dict < self.threshold:

            hash_input_key = hash(input_key)

            index = hash_input_key % self.initial_capacity

            if len(self.hash_table[index]) != 0:

                for i in range(len(self.hash_table[index])):

                    if list(self.hash_table[index][i])[0] == input_key:

                        self.hash_table[index][i] = (
                            input_key, input_value, hash_input_key
                        )
                        break
                else:
                    self.hash_table[index].append(
                        (input_key, input_value, hash_input_key)
                    )
                    self.current_len_of_dict += 1

            if len(self.hash_table[index]) == 0:

                self.hash_table[index].append(

                    (input_key, input_value, hash_input_key)
                )

                self.current_len_of_dict += 1

    def __getitem__(self, input_key: Union[int, float, str, object]) -> Any:
        """ x.__getitem__(y) <==> x[y] """

        hash_input_key = hash(input_key)
        index = hash_input_key % self.initial_capacity
        for key, value, hash_k in self.hash_table[index]:
            if key == input_key:
                return value
        raise KeyError("Dictionary missing key")

    def __len__(self) -> int:
        """ Return len(self). """
        return self.current_len_of_dict

    def __delitem__(self, input_key: Union[int, float, str, object]) -> None:
        """ Delete self[key]. """

        hash_input_key = hash(input_key)
        index = hash_input_key % self.initial_capacity
        for i in range(len(self.hash_table[index])):
            if list(self.hash_table[index][i])[0] == input_key:
                del self.hash_table[index][i]
                self.current_len_of_dict -= 1
                break

    def clear(self) -> None:
        """ D.clear() -> None.  Remove all items from D. """
        self.current_len_of_dict = 0
        self.initial_capacity = 8
        self.hash_table = [[] for i in range(self.initial_capacity)]
