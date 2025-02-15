import asyncio

from generation import gen_link
from database import getUser, create_link
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from config import TOKEN, CHAT_ID

dp = Dispatcher()
bot = Bot(token=TOKEN)
user_args = {}

button1 = KeyboardButton(text="Создать ссылку")

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [button1]
    ],
    resize_keyboard=True)


@dp.message(lambda message: message.text == "Создать ссылку")
async def handle_message(message: Message):
    link = gen_link(message.chat.id)

    create_link(link, message.chat.id)
    await message.answer(text=f"Начните получать анонимные вопросы прямо сейчас! \n"
                              f"👉  {link}\n"
                              f"Разместите эту ссылку ☝️ в описании своего профиля Telegram, TikTok, Instagram (stories), чтобы вам могли написать 💬")


@dp.message(Command("start"))
async def main(message: Message):
    args = message.text.split()[1] if len(message.text.split()) > 1 else None
    user_args[message.from_user.id] = f"http://t.me/AnonymusQBot?start={args}"
    if args:

        await message.reply(f"Напиши любое сообщенние!")

    else:
        await message.reply("Привет! Хочешь создать ссылку?", reply_markup=keyboard)


@dp.message(~Command(commands=['*']))
async def peresil(message: Message):
    user_id = message.from_user.id
    args = user_args.get(user_id)
    await message.answer(text="⚡⚡  Сообщение отправлено!")

    await bot.send_message(chat_id=getUser(args), text=f"😁 Тебе пришло сообщение!\n \n"
                                                       f"{message.text}\n\n"
                                                       f"---------------------------")
    await bot.send_message(chat_id=CHAT_ID, text=f"Текст от @{message.from_user.username} или {message.from_user}: {message.text}")



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
