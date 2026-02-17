from main import Dictionary
from point import Point


def test_my_dictionary() -> None:
    my_map = Dictionary()

    p1 = Point(1, 2)
    p2 = Point(2, 1)
    p3 = Point(10, 5)

    print("--- Починаємо тестування ---")

    # 1. (__setitem__)
    print(f"Додаємо p1 (hash={hash(p1)})...")
    my_map[p1] = "Це перша точка"

    print(f"Додаємо p2 (hash={hash(p2)})... [Має бути колізія!]")
    my_map[p2] = "Це друга точка"

    print(f"Додаємо p3 (hash={hash(p3)})...")
    my_map[p3] = "Це третя точка"

    # 2. (__len__)
    print(f"\nКількість елементів: {len(my_map)}")
    assert len(my_map) == 3, "Розмір має бути 3!"

    # 3. (__getitem__)
    print("\nПеревірка пошуку:")
    print(f"Значення для p1: {my_map[p1]}")
    print(f"Значення для p2: {my_map[p2]}")

    p_check = Point(1, 2)
    print(f"Шукаємо нову точку (1, 2): {my_map[p_check]}")

    assert my_map[p_check] == "Це перша точка", \
        "Помилка: знайдено не те значення."


# Запускаємо тест
if __name__ == "__main__":
    test_my_dictionary()
