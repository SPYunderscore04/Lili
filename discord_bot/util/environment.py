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
    def __init__(self) -> None:
        self.log_level: Final = get_env_var("LOG_LEVEL", "WARNING")
        self.db_url: Final = _fix_db_url(get_env_var("DB_URL"))
        self.discord_token: Final = get_env_var("DISCORD_TOKEN")
        self.target_guild: Final = get_env_var("TARGET_GUILD")
        self.hypixel_api_key: Final = get_env_var("HYPIXEL_API_KEY")


def _fix_db_url(db_url: str) -> str:
    if db_url.startswith("postgresql:"):
        db_url = "postgres:" + db_url[len("postgresql:") :]

    return db_url
