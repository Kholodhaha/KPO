import logging
import json
from aiogram import Bot, Dispatcher, executor, types
import requests

API_TOKEN = '5798218859:AAH7fJ5KhyVUbhyh6pKdgCkUTcqsj4gZlU4'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

binds = {}


@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(
        "!bind value\nupdate bind\n\n??\nshow binds\n\n,bind\nsearch by bind\n\n?bind\nremove bind\n\n.name\nsearch by collection")


@dp.message_handler()
async def echo(message: types.Message):
    if (message.text[0] == '!' and message.chat.id == -1001557635561):
        key, value = message.text[1:].split(' ')
        binds[value] = key
        await message.answer(f'Updated bind {key} = {value}')
    if (message.text[0] == '?' and message.chat.id == -1001557635561):
        if (message.text[1] == '?'):
            await message.answer(str(binds))
        else:
            key = message.text[1:]
            binds.pop(key)
            await message.answer(f'Cleared {key} from binds')
    if (message.text[0] == ',' and message.chat.id == -1001557635561):
        try:
            information = json.loads(
                requests.get(f'https://api-mainnet.magiceden.dev/v2/collections/{binds[message.text[1:]]}/stats').text)
            await message.answer(
                f"`Name:   {information['symbol']}`\n`Floor:  {int(information['floorPrice']) / 1000000000}`\n`Listed: {information['listedCount']}`",
                parse_mode='Markdown')
        except:
            pass
    if (message.text[0] == '.' and message.chat.id == -1001557635561):
        try:
            information = json.loads(
                requests.get(f'https://api-mainnet.magiceden.dev/v2/collections/{message.text[1:]}/stats').text)
            await message.answer(
                f"`Name:   {information['symbol']}`\n`Floor:  {int(information['floorPrice']) / 1000000000}`\n`Listed: {information['listedCount']}`",
                parse_mode='Markdown')
        except:
            pass


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
