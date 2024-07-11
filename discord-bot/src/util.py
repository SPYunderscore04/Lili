from logging import StreamHandler, Formatter, DEBUG, INFO, WARNING, ERROR, CRITICAL, getLevelName, basicConfig

from interactions import Embed, SlashContext


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

    basicConfig(level=getLevelName(log_level), handlers=[stdout_handler])


async def respond_eph(ctx: SlashContext, embed: Embed):
    await ctx.respond(embed=embed, ephemeral=True)


def cata_xp_to_next_level():
    xp_required = [
        50, 75, 110, 160, 230, 330, 470, 670, 950, 1340,
        1890, 2665, 3760, 5260, 7380, 10300, 14400, 20000, 27600, 38000,
        52500, 71500, 97000, 132000, 180000, 243000, 328000, 445000, 600000, 800000,
        1065000, 1410000, 1900000, 2500000, 3300000, 4300000, 5600000, 7200000, 9200000, 12000000,
        15000000, 19000000, 24000000, 30000000, 38000000, 48000000, 60000000, 75000000, 93000000, 116250000
    ]

    for xp in xp_required:
        yield xp

    while True:
        yield 200000000


def calculate_catacombs_level(experience: float) -> float:
    xp_iterator = cata_xp_to_next_level()

    level = 0
    for next_lvl_xp in xp_iterator:
        if experience < next_lvl_xp:
            return level + experience / next_lvl_xp

        level += 1
        experience -= next_lvl_xp
