from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Handlers.database import DatabaseControl
from Handlers.tasks import Task
from Handlers.until import JSONAnswer, User, Role
from loader import Program

bot = Program().bot

callbacks_router = Router()


@callbacks_router.callback_query(StateFilter(None))
async def callback(call: CallbackQuery):
    role = DatabaseControl().get_user(call.from_user.id)[1]  # Получаем роль пользоваеля
    user = User(call.from_user.id, Role[f'{role}'])  # Получаем класс пользователя
    if call.data == "_profile":
        # Профиль
        await bot.send_message(user.id, str(JSONAnswer("profile").get()).format(id=user.id, role=user.role.name))

    elif call.data == "_tasks":
        # Задачи
        tasks = DatabaseControl().get_tasks(user)
        if len(tasks) < 1:
            await bot.send_message(user.id, str(JSONAnswer("tasks_none").get()))
        else:
            keyboard = InlineKeyboardBuilder()

            for task in tasks:
                keyboard.add(InlineKeyboardButton(text=f"{task[2]} - {task[3]}", callback_data=f"_task|{task[0]}"))

            await bot.send_message(user.id, str(JSONAnswer("tasks").get()), reply_markup=keyboard.as_markup())

    elif "_task|" in call.data:
        #  Задача
        tasks = DatabaseControl().get_tasks(user)
        task = next((t for t in tasks if int(call.data.split("|")[1]) in t), None)
        if task is not None:
            task = Task(task[0], task[1], task[2], task[3])
            await bot.send_message(user.id, str(JSONAnswer("task").get()).format(name=task.name, status=task.status,
                                                                                 len_child=len(task.child_tasks)))
        else:
            await bot.send_message(user.id, str(JSONAnswer("except").get()))
