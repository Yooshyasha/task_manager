from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, StateFilter
from aiogram.utils.keyboard import (ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardButton,
                                    KeyboardButton)

from Handlers.database import DatabaseControl
from Handlers.until import JSONAnswer, User, Role

from loader import Program

bot = Program().bot

message_router = Router()


@message_router.message(CommandStart(), StateFilter(None))
async def start(message: Message):
    DatabaseControl().write_user(message.from_user.id)
    keyboard = InlineKeyboardBuilder().add(InlineKeyboardButton(text="Профиль", callback_data="_profile")).add(InlineKeyboardButton(text="Задачи", callback_data="_tasks"))
    await bot.send_message(message.from_user.id, str(JSONAnswer("start").get()), reply_markup=keyboard.as_markup())
