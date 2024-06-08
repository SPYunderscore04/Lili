import logging
import os
from logging import StreamHandler, Formatter, DEBUG, INFO, WARNING, ERROR, CRITICAL


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
    level_colours = [(DEBUG, '\033[0m'),
                     (INFO, '\033[34m'),
                     (WARNING, '\033[33m'),
                     (ERROR, '\033[31m'),
                     (CRITICAL, '\033[0;101m')]
    time = '\033[0;90m%(asctime)s\033[0m'
    level_name = '%(levelname)-8s'
    name = '\033[0;35m%(name)s\033[0m'
    message = '%(message)s'

    formatters = {level: Formatter(f'{time} {colour}{level_name}\033[0m {name}: {message}',
                                   '%Y-%m-%d %H:%M:%S')
                  for (level, colour) in level_colours}

    class ColouredLevelFormatter(Formatter):
        def format(self, record):
            return formatters[record.levelno].format(record)

    stdout_handler = StreamHandler()
    stdout_handler.setFormatter(ColouredLevelFormatter())

    # TODO file logger

    logging.basicConfig(level=log_level, handlers=[stdout_handler])
