from interactions import Client, AutoShardedClient, Intents

from environment import Environment

DiscordClient: Client = AutoShardedClient(token=Environment.DISCORD_TOKEN,
                                          debug_scope=Environment.DEBUG_SCOPE,
                                          delete_unused_application_commands=True,
                                          send_command_tracebacks=False,
                                          intents=Intents.ALL)  # TODO specify exact intents
