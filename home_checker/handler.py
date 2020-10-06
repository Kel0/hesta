import logging

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from settings import API_TOKEN

from .resources.responses import COMMANDS, WELCOME
from .states import GroupForm
from .utils import create_group, get_groups

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
    groups_in_text = md.text("No groups have found")
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
    await message.reply(
        "Please, enter the group name:", reply_markup=init_cancel_button()
    )


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
            "Group created successfully",
            reply_markup=keyboard_remove(),
        )
    else:
        await bot.send_message(
            message.chat.id, "Group hasn't been created", reply_markup=keyboard_remove()
        )
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
