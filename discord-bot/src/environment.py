import os
from typing import Final


def get_env_var(name: str, default: str = None) -> str:
    value = os.environ.get(name)

    match (value, default):
        case (None, None):
            raise RuntimeError(f"Environment variable {name} is not set")
        case (None, default):
            return default
        case (value, _):
            return value


class Environment:
    LOG_LEVEL: Final = get_env_var('LOG_LEVEL', 'WARNING')
    DB_URL: Final = get_env_var('DB_URL')
    DISCORD_TOKEN: Final = get_env_var('DISCORD_TOKEN')
    DEBUG_SCOPE: Final = get_env_var('DEBUG_SCOPE', '0')
    HYPIXEL_API_KEY: Final = get_env_var('HYPIXEL_API_KEY')
