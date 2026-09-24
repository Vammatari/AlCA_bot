import os
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from middlewares import AccessMiddleware
from clean_raw import schedule

load_dotenv()
router = Router()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(
    token=BOT_TOKEN, 
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
dp.message.middleware(AccessMiddleware())
dp.callback_query.middleware(AccessMiddleware())

# @dp.message(Command("start"))
# async def cmd_start(message: types.Message):
#     """Отправка кастомного эмодзи в тексте"""
#     # Заглушка ❤️ покажется, если у бота нет прав на кастомные эмодзи
#     text = f"Привет! Ты можешь отправть мне кастомный эмодзи, и я верну его ID.\n\n"
#     await message.answer(text)

def get_keys_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=key, callback_data=f"select:{key}")]
        for key in schedule.keys()
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# Клавиатура действия (Подтвердить / Назад)
def get_confirm_keyboard(key: str) -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(
                text="✅ Подтвердить", callback_data=f"confirm:{key}"
            ),
            InlineKeyboardButton(text="⬅️ Назад", callback_data="back"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


# Обработка команды /start
@router.message(Command("start"))
async def cmd_start(message: Message):
    print(f"Получена команда /start от {message.from_user.id}")  # 🔹 Лог в консоль
    await message.answer(
        "Выберите элемент из списка:",
        reply_markup=get_keys_keyboard(),
    )


# Обработка выбора ключа
@router.callback_query(F.data.startswith("select:"))
async def process_key_select(callback: CallbackQuery):
    key = callback.data.split(":", 1)[1]
    value = schedule.get(key, "Значение не найдено.")

    text = f"<b>Выбран элемент:</b> {key}\n\n<b>Текст для публикации:</b>\n{value}"
    await callback.message.edit_text(
        text=text,
        reply_markup=get_confirm_keyboard(key),
        parse_mode="HTML",
    )
    await callback.answer()


# Обработка кнопки "Назад"
@router.callback_query(F.data == "back")
async def process_back(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите элемент из списка:",
        reply_markup=get_keys_keyboard(),
    )
    await callback.answer()


# Обработка кнопки "Подтвердить" (Публикация в канал)
@router.callback_query(F.data.startswith("confirm:"))
async def process_confirm(callback: CallbackQuery, bot: Bot):
    key = callback.data.split(":", 1)[1]
    value = schedule.get(key)

    if value:
        # Отправка сообщения в канал
        await bot.send_message(chat_id=7359586185, text=value, parse_mode="HTML")

        # Ответ пользователю
        back_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ К списку", callback_data="back")]
            ]
        )
        await callback.message.edit_text(
            f"✅ Сообщение по ключу <b>«{key}»</b> успешно опубликовано в канал!",
            reply_markup=back_kb,
            parse_mode="HTML",
        )
        await callback.answer("Опубликовано!")
    else:
        await callback.answer("Ошибка: значение не найдено.", show_alert=True)



# @dp.message(F.text)
# async def catch_custom_emoji_id(message: types.Message):
#     """Ловит ID кастомного эмодзи, если он отправлен в тексте"""
#     if message.entities:
#         for entity in message.entities:
#             if entity.type == "custom_emoji":
#                 await message.answer(
#                     f"ID этого кастомного эмодзи:\n\n<code>{entity.custom_emoji_id}</code>"
#                 )
#                 return



async def main():

    print("🤖 Бот успешно запущен!")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())