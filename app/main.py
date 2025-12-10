from app.dictionary import Dictionary
from app.point import Point


if __name__ == "__main__":
    my_dict = Dictionary()

    my_dict[Point(1, 2)] = "Cache"
    my_dict[Point(993, -1)] = "Mirage"
    my_dict[Point(69, 67)] = "Inferno"

    for key, value in my_dict.items():
        print(key, value)
