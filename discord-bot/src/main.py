import logging
from asyncio import new_event_loop, set_event_loop

from tortoise import Tortoise

from discordclient import DiscordClient
from environment import Environment
from util import configure_logging


async def main():
    configure_logging(logging.getLevelName(Environment.LOG_LEVEL))
    logging.info('Starting')

    await Tortoise.init(db_url=Environment.DB_URL, modules={'models': ['model']})
    await Tortoise.generate_schemas()

    DiscordClient.load_extension('commands')
    await DiscordClient.astart(token=Environment.DISCORD_TOKEN)


async def on_shutdown():
    logging.info(f'Shutting down')
    await Tortoise.close_connections()


if __name__ == '__main__':
    loop = new_event_loop()
    set_event_loop(loop)

    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(on_shutdown())
