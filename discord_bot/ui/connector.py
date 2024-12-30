from copy import copy
from logging import getLogger
from typing import Callable, Coroutine

from interactions import SlashContext, Client, Member, SlashCommand

from discord_bot.application.linkingservice import LinkingService
from discord_bot.application.failure import Failure
from discord_bot.ui.command import Command
from discord_bot.ui.response import Response


class Connector:
    _log = getLogger(__name__)

    def __init__(self, linking_service: LinkingService):
        self._log.debug("Initialising")

        self._linking_service = linking_service
        self._commands: list[SlashCommand] = []

        self._bind_command(Command.link, self._on_link)
        self._bind_command(Command.unlink, self._on_unlink)
        self._bind_command(Command.force_link, self._on_force_link)
        self._bind_command(Command.force_unlink, self._on_force_unlink)

    def connect(self, discord_client: Client):
        self._log.info("Connecting bindings to Discord client")

        for command in self._commands:
            discord_client.add_interaction(command)

    async def _on_link(self, ctx: SlashContext, minecraft_username: str) -> None:
        await ctx.defer(ephemeral=True)
        await self._linking_service.link_member(ctx.author, minecraft_username)
        await ctx.send(embed=Response.Success.LINKED)

    async def _on_unlink(self, ctx: SlashContext) -> None:
        await ctx.defer(ephemeral=True)
        await self._linking_service.unlink_member(ctx.author)
        await ctx.send(embed=Response.Success.UNLINKED)

    async def _on_force_link(self, ctx: SlashContext, member: Member, minecraft_username: str) -> None:
        await ctx.defer(ephemeral=True)
        await self._linking_service.link_member(member, minecraft_username)
        await ctx.send(embed=Response.Success.LINKED)

    async def _on_force_unlink(self, ctx: SlashContext, member: Member) -> None:
        await ctx.defer(ephemeral=True)
        await self._linking_service.unlink_member(member)
        await ctx.send(embed=Response.Success.UNLINKED)

    async def _before_call(self, ctx: SlashContext, **kwargs) -> None:
        self._log.debug(f"@{ctx.author.username} called /{ctx.command.name} with {kwargs}")

    async def _on_error(self, error: Exception, ctx: SlashContext, **kwargs) -> None:
        self._log.debug(f"@{ctx.author.username} /{ctx.command.name} {kwargs} caused {error.__class__.__name__}")

        match error:
            case Failure() as f:
                await ctx.send(embed=f.response)

            case _:
                self._log.error(f"Unexpected error occurred!", exc_info=error)
                await ctx.send(embed=Response.Error.UNEXPECTED)

    def _bind_command(self, command: SlashCommand, callback: Callable[..., Coroutine]) -> None:
        self._log.debug(f"Binding /{command.name}")

        command = copy(command)
        command.callback = callback
        command.pre_run_callback = self._before_call
        command.error_callback = self._on_error

        self._commands.append(command)
