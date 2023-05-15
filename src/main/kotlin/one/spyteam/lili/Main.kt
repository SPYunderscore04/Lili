package one.spyteam.lili

import kotlinx.coroutines.runBlocking
import mu.KotlinLogging
import one.spyteam.lili.actions.HelpAction
import one.spyteam.lili.jooq.Tables.MEMBER


private val log = KotlinLogging.logger {}

fun main() = runBlocking {
    Database.selectFrom(MEMBER).fetch()
        .forEach {
            log.info { "Member: ${it.minecraftuuid} ${it.discordid}" }
        }

    DiscordBot.actions["help"] = HelpAction
    DiscordBot.start()
}
