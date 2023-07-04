import org.json.JSONArray

class DiscordApp(botToken: String) {

    private val api = RestApi(
        baseUrl = "https://discord.com/api/v10/",
        persistentHeaders = mapOf("Authorization" to "Bot $botToken")
    )

    val commands: JSONArray
        get() = api
            .get("applications/1106902553188372581/guilds/912005585766088704/commands")
            .use { JSONArray(it.body!!.string()) }
}
