import os
from dotenv import load_dotenv
import asyncio
import logging
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from aiogram.enums import ParseMode
from clean_raw import schedule
from format import format_data_value
from aiogram.client.default import DefaultBotProperties
load_dotenv()
# Укажите ваш токен и ID/username канала
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "-1003636581927"  # Или ID канала в формате -100XXXXXXXXXX

dp = Dispatcher()

# Словарь с данными
DATA = {
    "Новость 1": "🔥 Вышло важное обновление нашего сервиса!",
    "Акция": "⚡ Скидка 30% на все подписки до конца недели.",
    "Расписание": "📅 Ближайший прямой эфир состоится в пятницу в 18:00.",
}

router = Router()


# Клавиатура со списком всех ключей словаря
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
@router.message(CommandStart())
async def cmd_start(message: Message):
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
    raw_value = schedule.get(key)

    if raw_value:
        # 🔹 Преобразуем значение в строку перед отправкой в send_message
        text_to_send = format_data_value(raw_value)

        # Отправка строки в канал
        await bot.send_message(
            chat_id=CHANNEL_ID, text=text_to_send
        )

        back_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ К списку", callback_data="back")]
            ]
        )
        await callback.message.edit_text(
            f"✅ Сообщение по ключу <b>«{key}»</b> успешно опубликовано в канал!",
            reply_markup=back_kb
        )
        await callback.answer("Опубликовано!")
    else:
        await callback.answer("Ошибка: значение не найдено.", show_alert=True)


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())