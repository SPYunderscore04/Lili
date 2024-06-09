from interactions import Embed


def success_embed(title: str, description: str = None) -> Embed:
    return Embed(title=title, description=description, color=0x0066ff)


def error_embed(title: str, description: str = None) -> Embed:
    return Embed(title=title, description=description, color=0xff0000)


class Responses:
    class Success:
        LINKED = success_embed(
            'Account linked',
            'Your nickname will be set to your Minecraft name and Catacombs level.'
        )
        UNLINKED = success_embed(
            'Account unlinked',
            'Your nickname will no longer be updated.'
        )
        LINKED_ROLE_SET = success_embed(
            'Linked role updated',
            'Users with a linked Minecraft account will now receive this role.'
        )
        LINKED_ROLE_UNSET = success_embed(
            'Linked role removed',
            'Users with a linked Minecraft account no longer receive a role.'
        )
        LEVEL_ROLE_ADDED = success_embed(
            'Level role added',
            'Users with at least this Catacombs level will now receive this role.'
        )
        LEVEL_ROLE_REMOVED = success_embed(
            'Level role removed',
            'Users with no longer receive this role.'
        )
        LEVEL_ROLES_CLEARED = success_embed(
            'Level roles cleared',
            'Users will no longer receive any roles based on their Catacombs level.'
        )

    class Error:
        UNEXPECTED = error_embed(
            'Unexpected error',
            'Sorry, something went wrong. The developers have been informed.'
        )
        UNKNOWN_MINECRAFT_USERNAME = error_embed(
            'Unknown Minecraft username',
            'Please double-check your Minecraft name.'
        )
        MOJANG_API_REQUEST_FAILED = error_embed(
            'Mojang API request failed',
            'This is not your fault. The API might be down, please try again later.'
        )
        HYPIXEL_API_REQUEST_FAILED = error_embed(
            'Hypixel API request failed',
            'This is not your fault. The API might be down, please try again later.'
        )
        NO_DISCORD_USERNAME_LINKED = error_embed(
            'No Discord username linked',
            'Please link your Discord username to Hypixel. Click '
            '[here](https://www.google.com/search?q=how+to+link+discord+to+hypixel) '
            'to google instructions.'
        )
        WRONG_DISCORD_USERNAME_LINKED = error_embed(
            'Linked Discord username does not match',
            'Please make sure you linked the right Discord username to Hypixel. Click '
            '[here](https://www.google.com/search?q=how+to+link+discord+to+hypixel) '
            'to google instructions.'
        )
        NOT_LINKED = error_embed(
            'No Minecraft account linked',
            'You did not have a linked Minecraft account.'
        )
