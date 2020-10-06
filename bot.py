import logging

from aiogram import executor

from home_checker.handler import dp


logging.basicConfig(level=logging.INFO)
executor.start_polling(dp, skip_updates=True)
