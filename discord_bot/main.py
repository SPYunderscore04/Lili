import logging
from asyncio import TaskGroup, run, sleep

from interactions import Client, Intents
from tortoise import Tortoise

from discord_bot.application.hypixelapiservice import HypixelAPIService
from discord_bot.application.linkingservice import LinkingService
from discord_bot.application.memberupdateservice import MemberUpdateService
from discord_bot.application.mojangapiservice import MojangAPIService
from discord_bot.ui.connector import Connector
from discord_bot.util.environment import Environment
from discord_bot.util.logformatter import LogFormatter


class App:
    def __init__(self):
        self._env = Environment()
        self._configure_logging()

        self._create_discord_client()
        self._create_services()
        self._create_connectors()

    def _configure_logging(self) -> None:
        stdout_handler = logging.StreamHandler()
        stdout_handler.setFormatter(LogFormatter())

        # TODO file logger

        logging.getLogger().addHandler(stdout_handler)
        logging.getLogger().setLevel(logging.WARNING)
        logging.getLogger("discord_bot").setLevel(self._env.log_level)

    def _create_discord_client(self) -> None:
        self._discord_client = Client(
            token=self._env.discord_token,
            intents=Intents.ALL,  # TODO specify exact intents
            debug_scope=self._env.target_guild,  # forces all commands to be local to this guild
            delete_unused_application_commands=True,
            send_command_tracebacks=False,
            disable_dm_commands=True,
        )

    def _create_services(self) -> None:
        self._mojang_api = MojangAPIService()
        self._hypixel_api = HypixelAPIService(api_key=self._env.hypixel_api_key)

        self._member_update_service = MemberUpdateService(
            mojang_api=self._mojang_api,
            hypixel_api=self._hypixel_api,
            discord_client=self._discord_client,
        )
        self._linking_service = LinkingService(
            mojang_api=self._mojang_api,
            hypixel_api=self._hypixel_api,
            member_update_service=self._member_update_service,
        )

    def _create_connectors(self):
        self._connector = Connector(linking_service=self._linking_service)
        self._connector.connect(self._discord_client)

    async def start(self):
        async with TaskGroup() as tg:
            await self._initialise_orm()

            tg.create_task(self._discord_client.astart())

            while not self._discord_client.is_ready:
                await sleep(1)

            tg.create_task(self._run_update_loop())

    async def _initialise_orm(self) -> None:
        db_model_files = [
            "discord_bot.persistence.link",
        ]

        await Tortoise.init(db_url=self._env.db_url, modules={"models": db_model_files})
        await Tortoise.generate_schemas()

    async def _run_update_loop(self) -> None:
        retries_left = 3

        while retries_left > 0:
            try:
                await self._member_update_service.update_most_due_member()
                await sleep(60)  # TODO base on hypixel api limit

            except Exception as e:
                logging.error(f"Update loop crashed! {retries_left} tries remaining", exc_info=e)
                retries_left -= 1

        raise RuntimeError("Update loop failed")


if __name__ == "__main__":
    app = App()
    run(app.start())
