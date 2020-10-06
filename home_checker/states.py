from aiogram.dispatcher.filters.state import State, StatesGroup


class GroupForm(StatesGroup):
    group = State()


class StudentsForm(StatesGroup):
    group = State()


class CreateStudentForm(StatesGroup):
    group = State()


class Github(StatesGroup):
    group = State()
    repository = State()
