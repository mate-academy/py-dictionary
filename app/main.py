from typing import List, Any, Optional


class Dictionary:
    def __init__(self, elements: Optional[List[tuple]] = None) -> None:
        if elements is None:
            elements = []
        self.__bucket_size = 8
        self.__bucket_resize = self.__bucket_size * 2 / 3
        self.__length = 0
        self.__resize(len(elements))
        if len(elements):
            self.__assign_buckets(elements)

    def __resize(self, len_elements: int = 0) -> None:
        while len_elements > self.__bucket_resize:
            self.__bucket_size *= 2
            self.__bucket_resize = self.__bucket_size * 2 / 3

        self.__buckets = [[] for i in range(self.__bucket_size)]

    @staticmethod
    def __is_bucket_filled(bucket: tuple | list, eq: int = 1) -> bool:
        return len(bucket) == eq

    def __assign_buckets(self, elements: List[tuple]) -> None:
        for _key, _value in elements:

            if isinstance(_key, list | dict | set):
                raise TypeError(
                    f'The key can`t be like this: "{_key}" is "{type(_key)}"'
                )
            hashed_value = hash(_key)
            index = hashed_value % self.__bucket_size

            while self.__buckets[index]:
                if self.__buckets[index][0] == _key:
                    if self.__is_bucket_filled(self.__buckets[index]):
                        break
                    self.__length -= 1
                    break
                index = (index + 1) % self.__bucket_size

            self.__buckets[index] = (_key, _value,)
            self.__length += 1

    def __un_assign_buckets(self, _key: Any) -> None:
        hashed_value = hash(_key)
        index = hashed_value % self.__bucket_size

        while self.__buckets[index]:
            if self.__buckets[index][0] == _key:
                if self.__is_bucket_filled(self.__buckets[index]):
                    raise KeyError(f'There is no such key: "{_key}"')
                break
            index = (index + 1) % self.__bucket_size
        if not self.__buckets[index]:
            raise KeyError(f'There is no such key: "{_key}"')
        self.__buckets[index] = (_key,)
        self.__length -= 1

    def __get_buckets_full(self) -> list[Any]:
        return [
            full_bucket for full_bucket in self.__buckets
            if self.__is_bucket_filled(full_bucket, 2)
        ]

    def __rewrite_table(
            self,
            len_new_element: int,
    ) -> None:
        current_buckets = self.__get_buckets_full()

        self.__resize(self.__length + len_new_element)
        self.__length = 0
        self.__assign_buckets(current_buckets)

    def __setitem__(self, _key: Any, _value: Any) -> None:
        if self.__length + 1 > self.__bucket_resize:
            self.__rewrite_table(1)
        self.__assign_buckets([(_key, _value)])

    def __getitem__(self, input_key: Any) -> Any:
        hashed_value = hash(input_key)
        index = hashed_value % self.__bucket_size
        if input_key not in self.keys():
            raise KeyError(f'There is no such key: "{input_key}"')

        while self.__buckets[index]:
            _key = self.__buckets[index][0]
            if _key == input_key:
                if len(self.__buckets[index]) == 1:
                    raise KeyError(f'There is no such key: "{input_key}"')
                return self.__buckets[index][1]
            index = (index + 1) % self.__bucket_size

    def __delitem__(self, input_key: Any) -> None:
        self.__un_assign_buckets(input_key)

    def __str__(self) -> str:
        dict_str = "  {\n"
        for _key, _value in self.__get_buckets_full():
            dict_str += f"    {_key}: {_value},\n"
        dict_str += "}"
        return dict_str

    def __repr__(self) -> str:
        dict_repr = "{"
        for _key, _value in self.__get_buckets_full():
            dict_repr += f"{_key}: {_value}, "
        dict_repr += "}"
        return dict_repr

    def __len__(self) -> int:
        return self.__length

    def keys(self) -> list[Any]:
        return [_key for _key, _ in self.__get_buckets_full()]

    def values(self) -> list[Any]:
        return [_value for _, _value in self.__get_buckets_full()]

    def clear(self) -> None:
        self.__buckets = [[] for i in range(self.__bucket_size)]
        self.__length = 0

    def get(self, _key: Any) -> Any:
        _value = None
        try:
            _value = self[_key]
        except KeyError:
            return None
        return _value

    def update(self, elements: List[tuple]) -> None:
        if self.__length + len(elements) > self.__bucket_resize:
            self.__rewrite_table(len(elements))
        self.__assign_buckets(elements)
