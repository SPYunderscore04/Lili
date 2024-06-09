from interactions import Embed


def success_embed(title: str, description: str = None) -> Embed:
    return Embed(title=title, description=description, color=0x0000ff)


def error_embed(title: str, description: str = None) -> Embed:
    return Embed(title=title, description=description, color=0xff0000)


class Responses:
    class Success:
        LINKED = success_embed('Account Linked',
                               'Your nickname will be set to your Minecraft name and Catacombs level.')
        UNLINKED = success_embed('Account Unlinked',
                                 'Your nickname will no longer be updated.')
        LINKED_ROLE_SET = success_embed('Linked Role Updated',
                                        'Users with a linked Minecraft account will now receive this role.')
        LINKED_ROLE_UNSET = success_embed('Linked Role Removed',
                                          'Users with a linked Minecraft account no longer receive a role.')
        LEVEL_ROLE_ADDED = success_embed('Level Role Added',
                                         'Users with at least this Catacombs level will now receive this role.')
        LEVEL_ROLE_REMOVED = success_embed('Level Role Removed',
                                           'Users with no longer receive this role.')
        LEVEL_ROLES_CLEARED = success_embed('Level Roles Cleared',
                                            'Users will no longer receive any roles based on their Catacombs level.')

    class Error:
        UNEXPECTED = error_embed('Unexpected Error',
                                 'Sorry, something went wrong. The developers have been informed.')
