package service

import util.getEnvVariable
import util.lazyLogger

private val log by lazyLogger(Environment::class)

object Environment {
    val discordBotToken = getEnvVariable("DISCORD_BOT_TOKEN")

    init {
        log.trace { "Environment initialized" }
    }
}
