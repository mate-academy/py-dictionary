from __future__ import annotations
import dataclasses
from collections.abc import Hashable
from typing import Any


@dataclasses.dataclass
class Node:
    key: Hashable
    value: Any
    key_hash: int
    next_node: Node | None = None
