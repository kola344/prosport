import asyncio
from integrations.proxyapi import *
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import db

import config
import asyncio


class Bot:
    def __init__(self, token):
        self.vk = vk_api.VkApi(token=token)
        self.longpoll = VkLongPoll(self.vk)

    def run(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                self.handle_message(event)

    def handle_message(self, event):
        user_id = event.user_id  # Получаем идентификатор пользователя
        message = event.text

        # Отправка ответа
        generate_answer(user_id, message)

async def main():
    await db.initialize()
    bot = Bot(config.vk_token)
    bot.run()

if __name__ == '__main__':
    asyncio.run(main())