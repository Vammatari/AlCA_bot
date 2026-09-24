# from aiogram import BaseMiddleware
# from aiogram.types import Message
# from typing import Callable, Dict, Any, Awaitable

# ALLOWED_USER_IDS = [412164413,1532794560]

# class AccessMiddleware(BaseMiddleware):
#     async def __call__(
#         self,
#         handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
#         event: Message,
#         data: Dict[str, Any]
#     ) -> Any:
#         # Проверяем доступ
#         if event.from_user and event.from_user.id in ALLOWED_USER_IDS:
#             return await handler(event, data) # Пропускаем дальше
        
#         # Если доступа нет — отвечаем отказом и прерываем цепочку
#         if isinstance(event, Message):
#             await event.answer("⛔ У вас нет доступа к этому боту.")
#         return

import os
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable
from dotenv import load_dotenv

load_dotenv()

# Парсим разрешенные ID из .env
allowed_users_str = os.getenv("ALLOWED_USERS", "")
ALLOWED_USER_IDS = [
    int(user_id.strip()) 
    for user_id in allowed_users_str.split(",") 
    if user_id.strip().isdigit()
]

class AccessMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        # Получаем user_id в зависимости от типа события (сообщение или нажатие кнопки)
        user = event.from_user
        
        if user and user.id in ALLOWED_USER_IDS:
            # Если пользователь есть в списке — пропускаем к хендлерам
            return await handler(event, data)
        
        # Если доступа нет — блокируем и отправляем предупреждение
        if isinstance(event, Message):
            await event.answer("⛔ У вас нет доступа к этому боту.")
        elif isinstance(event, CallbackQuery):
            await event.answer("⛔ Нет доступа", show_alert=True)
            
        return  # Прерываем выполнение