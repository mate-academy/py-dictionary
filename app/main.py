from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.dict_as_list = [(), (), (), (), (), (), (), ()]
        self.cells = len(self.dict_as_list)
        self.max_elements = round(len(self.dict_as_list) * (2 / 3))
        self.length = 0

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if len(self.dict_as_list) - self.dict_as_list.count(
                ()) == self.max_elements:
            self.cells *= 2
            self.dict_as_list = self.restore_dict()
            self.max_elements = round(len(self.dict_as_list) * (2 / 3))

        self.add_elem_in_dict(key, value)

    def add_elem_in_dict(self, key: Hashable, value: Any) -> None:
        if not self.search_element(key) is None:
            self.dict_as_list[self.search_element(key)] = (key, hash(key),
                                                           value)
            return
        if not self.dict_as_list[hash(key) % self.cells]:
            self.dict_as_list[hash(key) % self.cells] = (key, hash(key),
                                                         value)
        else:
            count = 0
            while True:
                if not self.dict_as_list[count]:
                    self.dict_as_list[count] = (key, hash(key), value)
                    break
                count += 1
        self.length += 1

    def restore_dict(self) -> list:
        new_dict_as_list = [()] * self.cells

        for element in self.dict_as_list:
            if element:
                if not new_dict_as_list[hash(element[0]) % self.cells]:
                    new_dict_as_list[hash(element[0]) % self.cells] = element
                else:
                    count = 0
                    while True:
                        if not new_dict_as_list[count]:
                            new_dict_as_list[count] = element
                            break
                        count += 1

        return new_dict_as_list

    def search_element(self, key: Hashable) -> (int, None):
        if len(self.dict_as_list) - self.dict_as_list.count(()) > 0:
            count = 0
            while count != len(self.dict_as_list):
                if self.dict_as_list[count]:
                    if self.dict_as_list[count][0] == key:
                        return count
                count += 1
            return None

    def __getitem__(self, key: Hashable) -> Any:
        if self.dict_as_list[hash(key) % self.cells]:
            if self.dict_as_list[hash(key) % self.cells][0] == key:
                return self.dict_as_list[hash(key) % self.cells][2]

        if not (self.search_element(key) is None):
            return self.dict_as_list[self.search_element(key)][2]
        raise KeyError

    def __len__(self) -> int:
        return self.length

    def clear(self) -> None:
        self.__init__()

    def __delitem__(self, key: Hashable) -> None:
        self.dict_as_list[self.search_element(key)] = ()
        self.length -= 1

    def get(self, key: Hashable, value: Any = None) -> Any:
        if not (self.search_element(key) is None):
            return self.dict_as_list[self.search_element(key)][2]
        return value

    def pop(self, key: Hashable, default: Any = None) -> Any:
        element_index = self.search_element(key)

        if not (element_index is None):
            return_delete_key_value = self.dict_as_list[element_index][2]
            self.dict_as_list[element_index] = ()
            self.length -= 1

            return return_delete_key_value

        if not (default is None):
            return default
        raise KeyError

    def update(self,
               data: (list[tuple], dict, list[list], list[set])) -> None:
        if type(data) is dict:
            data = [(key, value) for key, value in data.items()]

        for item in data:
            self.__setitem__(item[0], item[1])

    def __iter__(self) -> dict:
        for element in self.dict_as_list:
            if element:
                yield {element[0]: element[2]}
