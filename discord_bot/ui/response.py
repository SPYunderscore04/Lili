from interactions import Embed


def success_embed(title: str, description: str = None) -> Embed:
    return Embed(title=title, description=description, color=0x0066FF)


def error_embed(title: str, description: str = None) -> Embed:
    return Embed(title=title, description=description, color=0xFF0000)


class Response:
    class Success:
        LINKED = success_embed(
            title="Account linked",
            description="You are now verified."
            " Your nickname will be set to your Minecraft name and Catacombs level.",
        )
        UNLINKED = success_embed(
            title="Account unlinked",
            description="You are no longer verified." " Your nickname will no longer be updated.",
        )

    class Error:
        UNEXPECTED = error_embed(
            title="Unexpected error",
            description="Whoops, something went wrong there. The developers have been informed.",
        )
        UNKNOWN_MINECRAFT_USERNAME = error_embed(
            title="Unknown Minecraft username",
            description="Please double-check your Minecraft name.",
        )
        MINECRAFT_API_REQUEST_FAILED = error_embed(
            title="Minecraft API request failed",
            description="This is not your fault. The API might be down, please try again later.",
        )
        HYPIXEL_API_REQUEST_FAILED = error_embed(
            title="Hypixel API request failed",
            description="This is not your fault. The API might be down, please try again later.",
        )
        NO_DISCORD_USERNAME_LINKED = error_embed(
            title="No Discord username linked",
            description="Please link your Discord username to Hypixel."
            "\nClick here:"
            " https://www.google.com/search?q=how+to+link+discord+to+hypixel"
            " to google instructions.",
        )
        WRONG_DISCORD_USERNAME_LINKED = error_embed(
            title="Linked Discord username does not match",
            description="Please make sure you linked the right Discord username to Hypixel."
            "\nClick here:"
            " https://www.google.com/search?q=how+to+link+discord+to+hypixel"
            " to google instructions.",
        )
        NOT_LINKED = error_embed(
            title="No Minecraft account linked",
            description="You did not have a Minecraft account linked to your Discord user.",
        )
        MEMBER_UPDATE_FAILED = error_embed(
            title="Member update failed",
            description="Please make sure this bot has sufficient permissions to perform the following actions:"
            "\n* Set nickname of {member} to {nickname}"
            "\n* Add roles {roles} to {member}",
        )
