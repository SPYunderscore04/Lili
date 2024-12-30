from logging import getLogger

from interactions import Member
from tortoise.expressions import Q
from tortoise.transactions import in_transaction

from discord_bot.application.failure import DiscordTagMismatch, NotLinked
from discord_bot.application.hypixelapiservice import HypixelAPIService
from discord_bot.application.memberupdateservice import MemberUpdateService
from discord_bot.application.mojangapiservice import MojangAPIService
from discord_bot.persistence.player import Player


class LinkingService:
    _log = getLogger(__name__)

    def __init__(self, mojang_api: MojangAPIService, hypixel_api: HypixelAPIService, member_update_service: MemberUpdateService):
        self._log.debug("Initialising")

        self._mojang_api = mojang_api
        self._hypixel_api = hypixel_api
        self._member_update_service = member_update_service

    async def link_member(self, member: Member, minecraft_name: str) -> None:
        self._log.info(f"Linking @{member.username} to {minecraft_name}")

        uuid, _ = await self._mojang_api.get_minecraft_profile(minecraft_name)
        discord_tag = await self._hypixel_api.get_linked_discord_tag(uuid)

        if member.username != discord_tag:
            raise DiscordTagMismatch

        discord_id = str(member.id)

        async with in_transaction():
            await Player.filter(Q(discord_id=discord_id) | Q(minecraft_uuid=uuid)).delete()
            await Player.create(minecraft_uuid=uuid, discord_id=discord_id)

        await self._member_update_service.update_member(member)

    async def unlink_member(self, member: Member) -> None:
        self._log.info(f"Unlinking @{member.username}")

        discord_id = str(member.id)

        if not await Player.exists(discord_id=discord_id):
            raise NotLinked

        async with in_transaction():
            await Player.filter(discord_id=discord_id).delete()

        await self._member_update_service.clean_member(member)
