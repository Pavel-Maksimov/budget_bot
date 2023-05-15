from dataclasses import dataclass


@dataclass
class Record:
    """
    Collect data of income or outcome to
      insert into database.
    """
    user_id: int
    type: str = None
    category: str = None
    amount: float = None
