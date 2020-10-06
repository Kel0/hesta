import logging
import re
from typing import Dict, List

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from settings import API_TOKEN

from .states import CreateStudentForm, GroupForm, StudentsForm

from .utils import (  # isort:skip
    create_group,
    formalize_students_text,
    get_groups,
    get_students,
    create_students,
)

from .resources.responses import (  # isort:skip
    COMMANDS,
    ENTER_GROUP_NAME,
    GROUP_FAIL,
    GROUP_SUCCESS,
    NO_GROUPS,
    NO_STUDENT,
    SEND_GROUP,
    WELCOME,
    ENTER_STUDENT,
    GROUP_NON,
    STUDENT_SUCCESS,
    STUDENT_FAIL,
    FAIL,
)

from .buttons import (  # isort:skip
    init_cancel_button,
    init_n_count_keyboard_buttons,
    init_welcome_help_buttons,
    keyboard_remove,
)

logger = logging.getLogger(__name__)


# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    reply_text = f"{WELCOME} \n\n{COMMANDS}"
    await message.answer(reply_text, reply_markup=init_welcome_help_buttons())


@dp.message_handler(commands=["groups_list"])
@dp.message_handler(Text(contains="Groups list", ignore_case=True))
async def handle_groups_list(message: types.Message):
    groups = await get_groups()
    groups_in_text = md.text(NO_GROUPS)
    keyboard = None
    groups_buttons = []
    groups_md_text = []

    if groups:
        for group in groups:
            groups_md_text.append(md.text(f"Name: {md.bold(group.group)}"))
            groups_buttons.append({"text": group.group})

        keyboard = init_n_count_keyboard_buttons(groups_buttons)
        groups_in_text = md.text(*groups_md_text, sep="\n")

    await message.answer(
        groups_in_text, reply_markup=keyboard, parse_mode=types.ParseMode.MARKDOWN
    )


@dp.message_handler(commands=["group"])
@dp.message_handler(Text(equals="Create group", ignore_case=True))
async def handle_group(message: types.Message):
    """
    Allow user to create groups

    :param message: Telegram chat's message
    :return:
    """
    # Set state
    await GroupForm.group.set()
    # Answer
    await message.reply(ENTER_GROUP_NAME, reply_markup=init_cancel_button())


@dp.message_handler(state=GroupForm.group)
async def process_group(message: types.Message, state: FSMContext):
    """
    Process group name

    :param message: Telegram chat's message
    :param state: Aiogram state
    :return:
    """
    async with state.proxy() as data:
        data["group"] = message.text

        status = await create_group(group_name=data["group"])

    if status:
        await bot.send_message(
            message.chat.id,
            GROUP_SUCCESS,
            reply_markup=keyboard_remove(),
        )
    else:
        await bot.send_message(
            message.chat.id, GROUP_FAIL, reply_markup=keyboard_remove()
        )
    await state.finish()


@dp.message_handler(commands=["students"])
@dp.message_handler(Text(contains="Get students", ignore_case=True))
async def handle_students(message: types.Message):
    """
    Allow user to get students of some group
    :param message: Telegram chat's message
    :return:
    """
    group_name: List[str] = re.findall(r"([\d]{1,3}\D+)", message.text)

    if len(group_name) > 0:
        group_name_str = group_name[0].upper()
        students = await get_students(group=group_name_str)
        if students is None:
            await message.reply(FAIL, reply_markup=types.ReplyKeyboardRemove())
            return

        text = formalize_students_text(students=students)
        await message.reply(text, reply_markup=types.ReplyKeyboardRemove())

    elif len(group_name) == 0:
        await StudentsForm.group.set()
        await message.reply(SEND_GROUP, reply_markup=init_cancel_button())


@dp.message_handler(state=StudentsForm.group)
async def process_students_by_group(message: types.Message, state: FSMContext):
    group_name = message.text.upper()
    students = await get_students(group=group_name)

    if students:
        text = formalize_students_text(students=students)
        await message.reply(text, reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.reply(NO_STUDENT, reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(commands=["create_students"])
async def handle_create_student(message: types.Message):
    await CreateStudentForm.group.set()
    await message.reply(ENTER_STUDENT, reply_markup=init_cancel_button())


@dp.message_handler(state=CreateStudentForm.group)
async def add_student(message: types.Message, state: FSMContext):
    students_list: List[Dict[str, str]] = [
        {
            "name": element.split("-")[0].strip(),
            "group": element.split("-")[1].strip().upper(),
            "link": element.split("-")[2].strip(),
        }
        for element in message.text.split(",")
    ]
    status = await create_students(students=students_list)

    if status == "No group":
        await message.reply(GROUP_NON, reply_markup=types.ReplyKeyboardRemove())
    elif status:
        await message.reply(STUDENT_SUCCESS, reply_markup=types.ReplyKeyboardRemove())
    elif status is None:
        await message.reply(STUDENT_FAIL, reply_markup=types.ReplyKeyboardRemove())

    await state.finish()


# You can use state '*' if you need to handle all states
@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(contains="cancel", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply("Cancelled.", reply_markup=types.ReplyKeyboardRemove())
