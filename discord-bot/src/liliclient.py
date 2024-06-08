from logging import getLogger
from discord import Client, Intents


class LiliClient(Client):
    __logger = getLogger(__qualname__)

    def __init__(self):
        self.__logger.info('Initialising')

        intents = Intents.default()
        intents.message_content = True

        super().__init__(intents=intents)

    async def on_ready(self):
        self.__logger.info(f'Ready, user is {self.user}')

    async def on_message(self, message):
        self.__logger.info(f'Message from {message.author}: {message.content}')
