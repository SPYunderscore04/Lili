package service

import io.ktor.client.*
import io.ktor.client.plugins.websocket.*
import io.ktor.client.request.*
import io.ktor.serialization.kotlinx.*
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking
import kotlinx.serialization.json.Json
import model.discord.gateway.Event
import util.lazyLogger

private val log by lazyLogger(DiscordGateway::class)

class DiscordGateway(url: String) {

    private val client = HttpClient {
        install(WebSockets) {
            contentConverter = KotlinxWebsocketSerializationConverter(Json)
        }
    }
    private val session = runBlocking { client.webSocketSession { url(url) } }

    init {
        log.info { "Initialising" }
        session.launch { sendQueuedMessages(session) }
        session.launch { receiveMessages(session) }
    }

    fun connect() {

    }

    private suspend fun sendQueuedMessages(session: DefaultClientWebSocketSession) {
        while (session.isActive) {
            // TODO
        }
    }

    private suspend fun receiveMessages(session: DefaultClientWebSocketSession) {
        while (session.isActive) {
            runCatching {
                session.receiveDeserialized<Event>()
            }.onSuccess {
                log.info { "Received: $it" }
            }.onFailure {
                log.error(it) { "Failed to receive message" }
            }
        }
    }
}
