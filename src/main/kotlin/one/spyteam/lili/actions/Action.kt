package one.spyteam.lili.actions

import dev.kord.core.event.interaction.GuildChatInputCommandInteractionCreateEvent
import dev.kord.rest.builder.interaction.ChatInputCreateBuilder

data class Action (
    val description: String,
    val helpText: String,
    val builder: ChatInputCreateBuilder.() -> Unit,
    val onInteraction: suspend (GuildChatInputCommandInteractionCreateEvent) -> Unit
)
