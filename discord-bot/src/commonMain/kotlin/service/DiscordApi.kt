package service

import io.ktor.client.*
import io.ktor.client.call.*
import io.ktor.client.plugins.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.client.plugins.logging.*
import io.ktor.client.request.*
import io.ktor.http.*
import io.ktor.http.HttpHeaders.Authorization
import io.ktor.serialization.kotlinx.json.*
import model.Environment
import model.discord.api.BotGatewayInfo
import util.lazyLogger

typealias Closure<T> = T.() -> Unit

private val log by lazyLogger(DiscordGateway::class)

object DiscordApi {

    suspend fun getBotGatewayInfo(): BotGatewayInfo {
        val result: BotGatewayInfo = getBody("gateway", "bot")
        // TODO
        return result
    }

    private suspend inline fun <reified T> getBody(vararg path: String): T =
        httpClient.get { url { path(*path) } }.body<T>()

    private val httpClient = buildHttpClient()
}

private fun buildHttpClient(): HttpClient {
    val loggerObject = object : Logger {
        override fun log(message: String) {
            log.trace { "HttpClient:" + "\n" + message.prependIndent() }
        }
    }

    val defaultRequestBuilder: Closure<DefaultRequest.DefaultRequestBuilder> = {
        url("https://discord.com/api/v10/")
        header(Authorization, "Bot ${Environment.discordBotToken}")
    }

    val loggingConfig: Closure<Logging.Config> = {
        level = LogLevel.ALL
        logger = loggerObject
    }

    val contentNegotiationConfig: Closure<ContentNegotiation.Config> = {
        json()
    }

    return HttpClient {
        expectSuccess = true
        defaultRequest(defaultRequestBuilder)
        install(Logging, loggingConfig)
        install(ContentNegotiation, contentNegotiationConfig)
    }
}
