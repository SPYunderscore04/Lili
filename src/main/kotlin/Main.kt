fun main() {
    val token = System.getenv("DISCORD_TOKEN")

    val api = DiscordApp(token)
    val cmdStr = api.commands.toString(4)
    println(cmdStr)

//    val applicationId = 1106902553188372581
//    val guildId = 912005585766088704
//    val path = "applications/$applicationId/guilds/$guildId/commands"
}
