import asyncio
import logging
from os import getenv
from clean_raw import schedule
from aiogram import Bot, Dispatcher, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from teams_config import TEAMS_DATA
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    LinkPreviewOptions,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from middlewares import AccessMiddleware
from aiogram.fsm.context import FSMContext
TOKEN = getenv("BOT_TOKEN")

# ──────────────────────────── РАСПИСАНИЕ ────────────────────────────
SCHEDULE =  schedule

# ──────────────────────────── ДАННЫЕ КОМАНД ────────────────────────────
TEAMS_DATA = TEAMS_DATA

CHANNEL_ID = getenv("CHANNEL_ID")



# ──────────────────────────── ХЕЛПЕРЫ ────────────────────────────



def team_display(team_name: str) -> str:
    canonical = team_name
    data = TEAMS_DATA.get(canonical)
    if not data:
        return team_name

    emoji = f'<tg-emoji emoji-id="{data["emoji_id"]}">🏈</tg-emoji>'

    if data["username"]:
        name_html = f'<a href="https://t.me/{data["username"]}">{canonical}</a>'
    else:
        name_html = canonical

    return f"{emoji} {name_html}"


def weeks_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for week in SCHEDULE.keys():
        kb.button(text=week, callback_data=f"week:{week}")
    kb.adjust(3)
    return kb.as_markup()


def back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="◀️ Назад", callback_data="back")]]
    )


def week_keyboard(week: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            # [InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"confirm:{week}")],
            [InlineKeyboardButton(text="◀️ Назад", callback_data="back")],
        ]
    )


def render_week(week: str, header: str | None = None) -> str:
    """Собирает текст недели: каждая пара команд — на своей строке."""
    matches = SCHEDULE.get(week, [])
    lines = [header or f"<b>{week}</b>"]
    if matches:
        header_emoji_id = "5375303625671216883"
        header_emoji = f'<tg-emoji emoji-id="{header_emoji_id}">🏈</tg-emoji>'
        lines.append(f"{header_emoji} Лига шагнула в {week} {header_emoji}\n")
        for match in matches:
            team1, team2 = match[0], match[1]
            lines.append(f"{team_display(team1)} @ {team_display(team2)}")
        lines.append("\nАнонсы матчей указывайте в комментариях к данному посту.")
    else:
        lines.append("")
        lines.append("Матчей нет.")
    return "\n".join(lines)


# ──────────────────────────── ХЕНДЛЕРЫ ────────────────────────────
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Выберите неделю:",
        reply_markup=weeks_keyboard(),
    )

@dp.message(Command("restart"))
async def cmd_restart(message: types.Message, state: FSMContext):
  # 1. Очищаем текущее состояние машины состояний (если оно было)
  await state.clear()

  # 2. Отправляем сообщение о перезапуске
  await message.answer(
      "🔄 Бот успешно перезапущен!\nВсе прошлые данные сессии сброшены."
  )

  # (Опционально) Можно сразу вызвать логику команды /start
  await message.answer("Введите /start для начала работы.")
@dp.callback_query(F.data.startswith("week:"))
async def show_week(callback: CallbackQuery):
    week = callback.data.split(":", 1)[1]

    if not SCHEDULE.get(week):
        await callback.message.edit_text(
            f"<b>{week}</b>\n\nМатчей нет.",
            reply_markup=back_keyboard(),
            link_preview_options=LinkPreviewOptions(is_disabled=True),
        )
        await callback.answer()
        return

    await callback.message.edit_text(
        render_week(week),
        reply_markup=week_keyboard(week),
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )
    await callback.answer()


@dp.callback_query(F.data == "back")
async def back_to_weeks(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите неделю:",
        reply_markup=weeks_keyboard(),
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )
    await callback.answer()


# @dp.callback_query(F.data.startswith("confirm:"))
# async def confirm_week(callback: CallbackQuery, bot: Bot):
#     week = callback.data.split(":", 1)[1]

#     # 1. Редактируем сообщение в чате с ботом
#     await callback.message.edit_text(
#         render_week(week, header=f"<b>{week}</b>"),
#         reply_markup=back_keyboard(),
#         link_preview_options=LinkPreviewOptions(is_disabled=True),
#     )

#     # 2. Публикуем в канал
#     try:
#         await bot.send_message(
#             chat_id=CHANNEL_ID,
#             text=render_week(week), #, header=f"🏈 <b>{week}</b>"),
#             link_preview_options=LinkPreviewOptions(is_disabled=True),
#         )
#         await callback.answer("Опубликовано в канал ✅")
#     except Exception as e:
#         logging.exception("Ошибка публикации в канал")
#         await callback.answer(f"Не удалось опубликовать: {e}", show_alert=True)


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

# ──────────────────────────── ЗАПУСК ────────────────────────────
async def main():
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp.message.middleware(AccessMiddleware())
    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())