import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, MessageEntity


BOT_TOKEN = "7359586185:AAFh0XtQkMYUjf9AkVwPQo2TJKxVqYtOTQI"
CHANNEL_ID = -1003636581927

CUSTOM_EMOJI_ID = "5253669314329879481"

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("test"))
async def test(message: Message):

    text = "🟣"

    entity = MessageEntity(
        type="custom_emoji",
        offset=0,
        length=2,  # 🟣 = 2 UTF-16 code units
        custom_emoji_id=CUSTOM_EMOJI_ID,
    )

    result = await bot.send_message(
        chat_id=CHANNEL_ID,
        text=text,
        entities=[entity],
    )

    print("Отправлено:")
    print(result)

    await message.answer("Отправлено в канал")


async def main():
    print("BOT STARTED")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())