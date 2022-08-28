import asyncio
import logging
from aiogram import Bot, Dispatcher, types
import validators
import subprocess
import os
import vlc
import time


logging.basicConfig(level=logging.INFO)
bot = Bot(token='5700629801:AAH08xK4NF0kpXE83pSbY1kZoEshGeSTVRA')
dp = Dispatcher()


@dp.message(commands=['start'])
async def start(message: types.Message):
    await message.reply("Hello, I'm a bot")

track = None


async def stop(message: types.Message):
    global track
    if track is not None:
        track.stop()
        track.release()
        track = None
dp.message.register(stop, commands=['stop'])


async def play(message: types.Message):
    global track
    file_id = message.text.split("=")[1]
    track = vlc.MediaPlayer(file_id + ".mp3")
    track.play()


async def link_answer(message: types.Message):
    content = message.text
    if validators.url(content):
        files = os.listdir(".")
        file_name = message.text.split("=")[1] + ".mp3"
        if not (file_name in files):
            await bot.send_message(message.chat.id, "ok, start downloading")
            bash_command = "youtube-dl -x --audio-format mp3 -o %(id)s.%(ext)s' " + content
            process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
        await bot.send_message(message.chat.id, "start playing")
        await play(message)
    else:
        await bot.send_message(message.chat.id, "not a link")
dp.message.register(link_answer)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
