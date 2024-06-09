from interactions import slash_command, SlashContext, slash_option, OptionType, Extension, Role, SlashCommand, \
    Permissions

from actions import *
from failures import Failure
from responses import Responses
from util import respond_eph


class Commands(Extension):
    _logger = getLogger(__qualname__)

    def __init__(self, _: Client):
        self._logger.info('Initialising')
        self.set_extension_error(self.on_error)
        self.add_ext_auto_defer(enabled=True, ephemeral=True, time_until_defer=1.5)

    @slash_command(name='link',
                   description='Link your Minecraft account to your Discord account')
    @slash_option(name='minecraft_name',
                  description='Your Minecraft username',
                  opt_type=OptionType.STRING,
                  required=True)
    async def on_link_called(self, ctx: SlashContext, minecraft_name: str):
        await link_account(minecraft_name, ctx.author.id)
        await respond_eph(ctx, Responses.Success.LINKED)

    @slash_command(name='unlink',
                   description='Unlink your Minecraft account from your Discord account')
    async def on_unlink_called(self, ctx: SlashContext):
        await unlink_account(ctx.author.id)
        await respond_eph(ctx, Responses.Success.UNLINKED)

    linked_role = SlashCommand(name='linked_role',
                               description='Configure role for linked users',
                               default_member_permissions=Permissions.ADMINISTRATOR)

    @linked_role.subcommand(sub_cmd_name='set',
                            sub_cmd_description='Set role for users with a linked Minecraft account')
    @slash_option(name='role',
                  description='Linked users will receive this role.',
                  opt_type=OptionType.ROLE)
    async def on_set_linked_role_called(self, ctx: SlashContext, role: Role):
        await set_linked_role(ctx.guild.id, role.id)
        await respond_eph(ctx, Responses.Success.LINKED_ROLE_SET)

    @linked_role.subcommand(sub_cmd_name='unset',
                            sub_cmd_description='Unset role for users with a linked Minecraft account')
    async def on_unset_linked_role_called(self, ctx: SlashContext):
        await remove_linked_role(ctx.guild.id)
        await respond_eph(ctx, Responses.Success.LINKED_ROLE_UNSET)

    level_roles = SlashCommand(name='level_roles',
                               description='Configure roles for users based on their Catacombs level',
                               default_member_permissions=Permissions.ADMINISTRATOR)

    @level_roles.subcommand(sub_cmd_name='add',
                            sub_cmd_description='Set role for users with a certain Catacombs level')
    @slash_option(name='role',
                  description='Role to give',
                  opt_type=OptionType.ROLE,
                  required=True)
    @slash_option(name='level',
                  description='Catacombs level required for this role',
                  opt_type=OptionType.NUMBER,
                  required=True)
    async def on_add_level_role_called(self, ctx: SlashContext, role: Role, level: float):
        await add_level_role(ctx.guild.id, role.id, level)
        await respond_eph(ctx, Responses.Success.LEVEL_ROLE_ADDED)

    @level_roles.subcommand(sub_cmd_name='remove',
                            sub_cmd_description='Remove a level role')
    @slash_option(name='role',
                  description='Role to remove',
                  opt_type=OptionType.ROLE,
                  required=True)
    async def on_remove_level_role_called(self, ctx: SlashContext, role: Role):
        await remove_level_role(ctx.guild.id, role.id)
        await respond_eph(ctx, Responses.Success.LEVEL_ROLE_REMOVED)

    @level_roles.subcommand(sub_cmd_name='clear',
                            sub_cmd_description='Remove all level roles')
    async def on_clear_level_roles_called(self, ctx: SlashContext):
        await clear_level_roles(ctx.guild.id)
        await respond_eph(ctx, Responses.Success.LEVEL_ROLES_CLEARED)

    async def on_error(self, error: Exception, ctx: SlashContext, **kwargs):
        command = ctx.command.name

        if isinstance(error, Failure):
            self._logger.info(f'{command} failed with {error}')
            await respond_eph(ctx, error.embed())

        else:
            self._logger.error(f'Exception occurred during {command} {kwargs}', exc_info=error)
            await respond_eph(ctx, Responses.Error.UNEXPECTED)
