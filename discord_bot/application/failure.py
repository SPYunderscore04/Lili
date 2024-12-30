from abc import ABC

from interactions import Embed, Role, Member

from discord_bot.ui.response import Response


class Failure(Exception, ABC):
    response: Embed


class UnknownMinecraftUsername(Failure):
    response = Response.Error.UNKNOWN_MINECRAFT_USERNAME


class NoDiscordTagLinked(Failure):
    response = Response.Error.NO_DISCORD_USERNAME_LINKED


class DiscordTagMismatch(Failure):
    response = Response.Error.WRONG_DISCORD_USERNAME_LINKED


class NotLinked(Failure):
    response = Response.Error.NOT_LINKED


class MojangAPIRequestFailed(Failure):
    response = Response.Error.MOJANG_API_REQUEST_FAILED


class HypixelAPIRequestFailed(Failure):
    response = Response.Error.HYPIXEL_API_REQUEST_FAILED


class MemberUpdateFailed(Failure):
    response = Response.Error.MEMBER_UPDATE_FAILED

    def __init__(self, member: Member, nickname: str, roles: list[Role]):
        self.response.description = self.response.description.format(
            member=member.mention,
            nickname=nickname,
            roles=", ".join(r.mention for r in roles),
        )
