from dataclasses import dataclass
from typing import Collection


@dataclass
class Record:
    user_id: int
    type: str = None
    category: str = None
    amount: float = None
