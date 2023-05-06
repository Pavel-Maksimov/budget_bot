import json
from typing import Collection


def create_keyboard(columns: int,
                    buttons: Collection[str],
                    resize_keyboard: bool = True,
                    one_time_keyboard: bool = True) -> str:
    keyboard = []
    keyboard.append([{"text": "⇦"}])
    keyboard[0].extend(
        [
            {"text": buttons[i]} for i in range(min(columns-1, len(buttons)))
        ]
    )
    idx = columns - 1
    while idx < len(buttons):
        left = idx
        idx += columns
        row = [
            {"text": buttons[i]} for i in range(left, min(idx, len(buttons)))
        ]
        keyboard.append(row)
    return json.dumps(
        {"keyboard": keyboard,
         "resize_keyboard": resize_keyboard,
         "one_time_keyboard": one_time_keyboard},
        ensure_ascii=True
    )
