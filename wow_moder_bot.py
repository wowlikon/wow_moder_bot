import logging, mmap
from aiogram import Bot, Dispatcher, executor, types
import aiogram.utils.markdown as ftm
from filter import IsAdminFilter

TOKEN = "5037292962:AAG3TPthGRs-FUQmCQ940ARL8nNMnHK8HC8"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

dp.filters_factory.bind(IsAdminFilter)

@dp.message_handler(commands=['id'], commands_prefix = '!/')
async def cmd_id(message: types.Message):
    print(message)
    await message.answer(message.from_user.id)

@dp.message_handler(commands=['echo'], commands_prefix = '!/')
async def cmd_echo(message: types.Message):
    text = message.text.split()[1:]
    text_str = " ".join(text)
    print(text)
    print(text_str)
    await message.delete()
    await message.answer(text_str)

@dp.message_handler(content_types = ["new_chat_members"])
async def on_user_joined(message: types.Message):
    print(message)
    await message.delete()
    user = message.new_chat_members
    await message.answer("Добро пожаловать в чат " + str(message.chat.title) + ", " + user[0]["first_name"])

@dp.message_handler(is_admin = True, commands = ["ban"], commands_prefix="!/")
async def cmd_ban(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Это команда работает только как ответ!")
        return

    await message.bot.delete_message(message.chat.id, message.message_id)
    await message.bot.kick_chat_member(chat_id = message.chat.id, user_id = message.reply_to_message.from_user.id)
    await message.reply_to_message.reply(
        ftm.text(
            ftm.text(ftm.hboild("Вам бан")),
            ftm.text(ftm.hunderline("/n от Админа")),
            sep = "\n"), parse_mode = "HTML")

@dp.message_handler()
async def filter_message(message: types.Message):
    text = message.text.lower().split()
    print(message)
    cens = open('cens.txt', 'r', encoding='utf-8').read().splitlines()
    if len(message.text) > 100:
        await message.reply("Слишком большое сообщение\!", parse_mode = "MarkdownV2")
        print("Слишком большое сообщение!")
    for word in cens:
        delete = (word in text)
        if delete:
            await message.reply("__**Добавьте '||'**__")
        if (delete and not message.entities != []) or len(message.text) > 100:
            await message.delete()
            break

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)