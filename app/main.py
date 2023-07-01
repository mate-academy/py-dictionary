from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.stored_data = []

    def __str__(self) -> str:
        representation = "{"
        for current_pair in self.stored_data:
            key, value = current_pair
            representation += f"'{key}': '{value}', "
        representation = representation[:-2]
        representation += "}"
        return representation

    def __setitem__(self, key: Hashable, value: Any) -> None:
        for current_pair in self.stored_data:
            if current_pair[0] == key:
                current_pair[1] = value
                return None

        self.stored_data.append([key, value])

    def __getitem__(self, key: Hashable) -> Any:
        for current_pair in self.stored_data:
            cur_key, cur_value = current_pair
            if key == cur_key:
                return cur_value

        raise KeyError

    def __len__(self) -> int:
        return len(self.stored_data)

    def clear(self) -> None:
        self.stored_data = []

    def __delitem__(self, key: Hashable) -> Any:
        for current_pair in self.stored_data:
            if key == current_pair[0]:
                returned_value = current_pair[1]
                self.stored_data.remove(current_pair)
                return returned_value

    def get(self, key: Hashable) -> Any:
        return self.__getitem__(key)

    def pop(self, key: Hashable) -> Any:
        return self.__delitem__(key)

    def update(self, appended_dictionary: dict) -> None:
        if not isinstance(appended_dictionary, dict):
            raise ValueError
        for key, value in appended_dictionary.items():
            validator = False
            for current_pair in self.stored_data:
                current_key, current_value = current_pair
                if key == current_key:
                    current_pair[1] = value
                    validator = True
                    break
            if validator is False:
                self.stored_data.append([key, value])

    def __iter__(self) -> None:
        yield from (current_pair[0] for current_pair in self.stored_data)
