def create_keyboard(columns: int, buttons: list):
    keyboard = []
    idx = 0
    while idx < len(buttons):
        left = idx
        idx += columns
        row = [{"text": buttons[i]} for i in range(left, min(idx, len(buttons)))]
        keyboard.append(row)
    return {"keyboard": keyboard, "resize_keyboard": True, "one_time_keyboard": True}
