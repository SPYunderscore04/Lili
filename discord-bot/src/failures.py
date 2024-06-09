from interactions import Embed

from responses import Responses


class Failure(RuntimeError):
    def embed(self) -> Embed:
        raise NotImplementedError

    def __str__(self):
        return self.__class__.__name__


class UnknownMinecraftUsername(Failure):
    def embed(self) -> Embed:
        return Responses.Error.UNKNOWN_MINECRAFT_USERNAME


class MojangApiRequestFailed(Failure):
    def embed(self) -> Embed:
        return Responses.Error.MOJANG_API_REQUEST_FAILED


class HypixelApiRequestFailed(Failure):
    def embed(self) -> Embed:
        return Responses.Error.HYPIXEL_API_REQUEST_FAILED


class NoDiscordUsernameLinked(Failure):
    def embed(self) -> Embed:
        return Responses.Error.NO_DISCORD_USERNAME_LINKED


class WrongDiscordUsernameLinked(Failure):
    def embed(self) -> Embed:
        return Responses.Error.WRONG_DISCORD_USERNAME_LINKED


class NotLinked(Failure):
    def embed(self) -> Embed:
        return Responses.Error.NOT_LINKED
