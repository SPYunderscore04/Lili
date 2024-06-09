import logging
import os
from logging import StreamHandler, Formatter, DEBUG, INFO, WARNING, ERROR, CRITICAL

from interactions import Embed, SlashContext


def get_env_var(name: str, default: str = None) -> str:
    value = os.environ.get(name)

    match (value, default):
        case (None, None):
            raise RuntimeError(f"Environment variable {name} is not set")
        case (None, default):
            return default
        case (value, _):
            return value


def configure_logging(log_level: int):
    blue = '\033[0;34m'
    yellow = '\033[0;33m'
    red = '\033[0;31m'
    red_bg = '\033[0;101m'
    black = '\033[0;90m'
    purple = '\033[0;35m'
    reset = '\033[0m'

    level_colours = [(DEBUG, reset),
                     (INFO, blue),
                     (WARNING, yellow),
                     (ERROR, red),
                     (CRITICAL, red_bg)]

    time = f'{black}%(asctime)s{reset}'
    name = f'{purple}%(name)s{reset}'
    message = f'%(message)s{reset}'
    level_name = f'%(levelname)-8s{reset}'

    formatters = {level: Formatter(f'{time} {colour}{level_name} {name}: {message}',
                                   '%Y-%m-%d %H:%M:%S')
                  for (level, colour) in level_colours}

    class ColouredLevelFormatter(Formatter):
        def format(self, record):
            return formatters[record.levelno].format(record)

    stdout_handler = StreamHandler()
    stdout_handler.setFormatter(ColouredLevelFormatter())

    # TODO file logger

    logging.basicConfig(level=log_level, handlers=[stdout_handler])


async def respond_eph(ctx: SlashContext, embed: Embed):
    await ctx.respond(embed=embed, ephemeral=True)
