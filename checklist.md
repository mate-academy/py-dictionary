# Check Your Code Against the Following Points

## Code Style

Make sure that you provide message when exception raises.

## Code Efficiency

1) Make sure that your methods work with 
**O(1)** time complexity in the best variant and 
**O(n)** i the worst (because of collision handling).

The exceptions:
- `__init__` and `clear` methods alvays have O(n) time complexity
- resizing the dictionary works with
**O(n)** time complexity in the best variant and 
**O(n^2)** i the worst (because of collision handling).


Good example:


```python
class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * 8
        
    # in any method that add or delete item we change self.length

    def __len__(self) -> int:
        return self.length
```

Bad example:

```python
class Dictionary:
    def __init__(self) -> None:
        self.hash_table: list = [None] * 8

    def __len__(self) -> int:
        return len([cell for cell in self.hash_table if cell])
```

**Note:** loops have O(n) time complexity, 
but can achieve O(1) in the best case 
(list comprehension is also a loop)

2) If you want check your `__delitem__` method 
uncomment `test_deletion():` test in `./tests/test_main.py`

**Note:** `__delitem__` should return nothing.

## Clean Code

Add comments, prints, and functions to check your solution when you write your code. 
Don't forget to delete them when you are ready to commit and push your code.
