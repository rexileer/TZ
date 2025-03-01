from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Catalog"),
            KeyboardButton(text="Cart"),
        ],
        [
            KeyboardButton(text="FAQ"),
            KeyboardButton(text="?"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Choose action from menu",
    selective=True
)