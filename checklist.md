# Check Your Code Against the Following Points

## Code Style

Make sure that you provide message when exception rises.

## Code Efficiency

### Make sure that your methods work with **O(1)** time complexity.

The exceptions:
- `__init__` and `clear` methods 
- handling the collision in any method
- resizing the dictionary

Bad example:

```python
class Dictionary:
    def __init__(self) -> None:
        self.hash_table: list = [None] * 8

    def __len__(self) -> int:
        return len([cell for cell in self.hash_table if cell])
```

**Note:** any loop have O(n) time complexity (list comprehension is also a loop)

## Clean Code

Add comments, prints, and functions to check your solution when you write your code. 
Don't forget to delete them when you are ready to commit and push your code.
