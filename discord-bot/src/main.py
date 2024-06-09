import logging
from asyncio import new_event_loop, set_event_loop
from interactions import AutoShardedClient
from tortoise import Tortoise

from util import get_env_var, configure_logging


async def main():
    log_level = get_env_var('LOG_LEVEL', 'WARNING')
    configure_logging(logging.getLevelName(log_level))

    logging.info('Starting')

    db_url = get_env_var('DB_URL')
    await Tortoise.init(db_url=db_url, modules={'models': ['model']})
    await Tortoise.generate_schemas()

    discord_token = get_env_var('DISCORD_TOKEN')
    debug_scope = get_env_var('DEBUG_SCOPE', None)

    client = AutoShardedClient(debug_scope=debug_scope, send_command_tracebacks=False)
    client.load_extension('commands')
    await client.astart(token=discord_token)


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
