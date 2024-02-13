package service

import io.github.oshai.kotlinlogging.KLogger
import io.ktor.client.*
import io.ktor.client.call.*
import io.ktor.client.plugins.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.client.plugins.logging.*
import io.ktor.client.request.*
import io.ktor.http.*
import io.ktor.http.HttpHeaders.Authorization
import io.ktor.serialization.kotlinx.json.*
import model.discord.api.BotGatewayInfo
import util.getEnvVariable
import util.getLogger

object DiscordApi {
    suspend fun getBotGatewayInfo(): BotGatewayInfo {
        val result: BotGatewayInfo = getBody("gateway", "bot")
        // TODO
        return result
    }

    private suspend inline fun <reified T> getBody(vararg path: String): T =
        httpClient.get { url { path(*path) } }.body<T>()

    private val log = getLogger(this)
    private val httpClient = getHttpClient(log)
}

private fun getHttpClient(log: KLogger): HttpClient {
    val botToken = getEnvVariable("DISCORD_BOT_TOKEN")
    val loggerObj = object : Logger {
        override fun log(message: String) = log.debug { "HttpClient:" + "\n" + message.prependIndent() }
    }

    return HttpClient {
        expectSuccess = true
        defaultRequest {
            url("https://discord.com/api/v10/")
            header(Authorization, "Bot $botToken")
        }
        install(Logging) {
            level = LogLevel.ALL
            logger = loggerObj
        }
        install(ContentNegotiation) { json() }
    }
}
