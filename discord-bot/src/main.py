import os
import discord.utils

from liliclient import LiliClient


def main():
    discord.utils.setup_logging()

    token = os.environ.get('DISCORD_TOKEN')
    client = LiliClient()
    client.run(token)


if __name__ == '__main__':
    main()
