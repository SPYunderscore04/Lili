package one.spyteam.lili.actions

import dev.kord.core.behavior.interaction.response.respond
import dev.kord.rest.builder.interaction.string
import one.spyteam.lili.DiscordBot

private fun getCommandsOverview(): String {
    return buildString {
        appendLine("__**Commands Overview**__")
        DiscordBot.actions.forEach { (name, action) ->
            appendLine("`/$name`: ${action.description}")
        }
    }
}

private fun getHelpFor(commandName: String): String {
    return DiscordBot.actions[commandName]?.let {
        buildString {
            appendLine("__**Help for:**__")
            appendLine("```/$commandName```")
            appendLine("> ")
            appendLine("> ${it.description}")
            it.helpText.lines().forEach { line ->
                appendLine("> $line")
            }
        }
    } ?: throw IllegalArgumentException("No such command: $commandName")
}

val helpAction = Action(
    "Get additional information about commands",
    "Gives an overview of all commands, or detailed information about a specific command",
    {
        string("command", "The command to get help for") {
            required = false
            DiscordBot.actions.forEach { (name, _) -> choice(name, name) }
        }
    },
    { event ->
        val defer = event.interaction.deferEphemeralResponse()
        val commandName = event.interaction.command.strings["command"]
        val response = commandName
            ?.let { getHelpFor(it) }
            ?: getCommandsOverview()
        defer.respond { content = response }
    }
)
