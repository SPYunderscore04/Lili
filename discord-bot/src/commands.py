from interactions import slash_command, SlashContext, slash_option, OptionType, Extension, Role, SlashCommand, \
    Permissions, Client

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
        await link_account(minecraft_name, ctx.author)
        await respond_eph(ctx, Responses.Success.LINKED)

    @slash_command(name='unlink',
                   description='Unlink your Minecraft account from your Discord account')
    async def on_unlink_called(self, ctx: SlashContext):
        await unlink_account(ctx.author)
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
        await set_linked_role(ctx.guild, role.id)
        await respond_eph(ctx, Responses.Success.LINKED_ROLE_SET)

    @linked_role.subcommand(sub_cmd_name='unset',
                            sub_cmd_description='Unset role for users with a linked Minecraft account')
    async def on_unset_linked_role_called(self, ctx: SlashContext):
        await remove_linked_role(ctx.guild)
        await respond_eph(ctx, Responses.Success.LINKED_ROLE_UNSET)

    async def on_error(self, error: Exception, ctx: SlashContext, **kwargs):
        command = ctx.command.name

        if isinstance(error, Failure):
            self._logger.info(f'/{command} failed with {error}', exc_info=error.__cause__)
            await respond_eph(ctx, error.embed())

        else:
            self._logger.error(f'Exception occurred during /{command} {kwargs}', exc_info=error)
            await respond_eph(ctx, Responses.Error.UNEXPECTED)
