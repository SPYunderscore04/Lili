package one.spyteam.lili

import dev.kord.core.Kord
import dev.kord.core.behavior.createChatInputCommand
import dev.kord.core.event.interaction.GuildChatInputCommandInteractionCreateEvent
import dev.kord.core.on
import kotlinx.coroutines.runBlocking
import mu.KotlinLogging
import one.spyteam.lili.actions.Action

object DiscordBot {
    val actions = mutableMapOf<String, Action>()

    private val log = KotlinLogging.logger { }
    private val kord = runBlocking { Kord(System.getenv("DISCORD_TOKEN")) }

    init {
        log.info { "Initializing" }

        // event handlers
        kord.on<GuildChatInputCommandInteractionCreateEvent> { handleCommandEvent(this) }
    }

    suspend fun start() {
        log.info { "Starting" }
        registerActions()
        kord.login()
    }

    suspend fun stop() {
        log.info { "Stopping" }
        kord.shutdown()
    }

    suspend fun registerActions() {
        kord.guilds.collect { guild ->
            actions.forEach { (name, action) ->
                guild.createChatInputCommand(
                    name,
                    action.description,
                    action.builder
                )
            }
        }
    }

    private suspend fun handleCommandEvent(event: GuildChatInputCommandInteractionCreateEvent) {
        val name = event.interaction.command.rootName
        actions[name]?.let {
            log.info { "Received command: $name ${event.interaction.command.options}" }
            it.onInteraction(event)
        } ?: log.warn { "Received unknown command: $name" }
    }
}
