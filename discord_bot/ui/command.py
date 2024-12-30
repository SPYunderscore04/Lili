from typing import Final

from interactions import SlashCommand, SlashCommandOption, OptionType, Permissions


class Command:
    link: Final = SlashCommand(
        name="link",
        description="Link your Minecraft account to your Discord account",
        options=[
            SlashCommandOption(
                name="minecraft_username",
                description="Your Minecraft username",
                type=OptionType.STRING,
                max_length=16,
            )
        ],
    )

    unlink: Final = SlashCommand(
        name="unlink",
        description="Unlink your Minecraft account from your Discord account",
    )

    force_link: Final = SlashCommand(
        name="force_link",
        description="Manually link a member (if API is broken / member refuses to use it / member too dumb)",
        options=[
            SlashCommandOption(
                name="member",
                description="Discord member to link",
                type=OptionType.USER,
            ),
            SlashCommandOption(
                name="minecraft_username",
                description="Minecraft username of that member",
                type=OptionType.STRING,
                max_length=16,
            ),
        ],
        default_member_permissions=Permissions.MANAGE_ROLES,
    )

    force_unlink: Final = SlashCommand(
        name="force_unlink",
        description="Manually unlink a member's minecraft account (if they lost access to that Discord account)",
        options=[
            SlashCommandOption(
                name="member",
                description="Discord member to unlink",
                type=OptionType.USER,
            ),
        ],
        default_member_permissions=Permissions.MANAGE_ROLES,
    )
