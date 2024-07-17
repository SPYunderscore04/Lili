from logging import getLogger

from interactions import Task, IntervalTrigger, Extension, Client
from actions import update_guild_members


class Tasks(Extension):
    _logger = getLogger(__qualname__)

    def __init__(self, _: Client):
        self._logger.info('Initialising')
        self.update_all_guilds_and_members.start()

    @Task.create(IntervalTrigger(minutes=15))
    async def update_all_guilds_and_members(self):
        self._logger.info('Running scheduled update of all guilds and members')
        await update_guild_members()
