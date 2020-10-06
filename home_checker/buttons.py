from aiogram.types import (  # isort:skip
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)


def init_welcome_help_buttons() -> ReplyKeyboardMarkup:
    create_group = KeyboardButton(text="Create group")
    create_students = KeyboardButton(text="Create students")
    get_groups = KeyboardButton(text="Get groups list")
    get_students = KeyboardButton(text="Get students list")
    check_commits = KeyboardButton(text="Check for commit")

    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(get_groups)
    kb.add(get_students)
    kb.add(create_group)
    kb.add(create_students)
    kb.add(check_commits)
    return kb


def init_cancel_button() -> ReplyKeyboardMarkup:
    button_cancel = KeyboardButton(text="Cancel ❌")

    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(button_cancel)
    return kb


def init_n_count_keyboard_buttons(buttons: list, prefix: str) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3)
    button_n = [
        eval(f"KeyboardButton(text='{prefix} {button['text']}')") for button in buttons
    ]
    kb.add(*button_n)
    return kb


def keyboard_remove() -> ReplyKeyboardRemove:
    kb = ReplyKeyboardRemove()
    return kb
