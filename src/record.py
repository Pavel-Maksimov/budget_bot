from dataclasses import dataclass


@dataclass
class Record:
    user_id: int
    type: str = None
    category: str = None
    amount: float = None
